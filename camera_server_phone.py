#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Compagnon ReloadAtlas — diffuse la camera du smartphone vers le PC.

A executer DIRECTEMENT sur le smartphone avec Pydroid 3 (voir
README_INSTALLATION.md) ; aucun pip n'est necessaire sur le telephone, les
API Android sont accedees par pyjnius (fourni avec Pydroid 3).

Modes :
  python camera_server_phone.py tcp             serveur WiFi (hotspot ou box)
  python camera_server_phone.py bt              serveur Bluetooth (RFCOMM)
  python camera_server_phone.py selftest        serveur TCP + frames de test,
                                                executable sur un PC pour
                                                valider le module de bout en
                                                bout (mode --self-test du plan)
  python camera_server_phone.py --list-cameras  liste les cameras du telephone

Options : --port 8899 --fps 8 --size 320x240 --quality 60 --camera-id 0

Protocole (identique a protocol.py du module PC — a garder synchronise) :
  handshake "RA-CAM v1\\n" + "INFO {json}\\n"
  trames "FRAME <n>\\n" + n octets JPEG
  commandes "SET quality|size|fps=v", "PING" -> "PONG <ms>"
  decouverte UDP : sonde "RA-CAM-DISCOVER v1" -> "RA-CAM-HERE v1 <port> <nom>"
"""

import argparse
import json
import queue
import socket
import sys
import threading
import time

PROTOCOL_NAME = "RA-CAM"
PROTOCOL_VERSION = 1
HANDSHAKE_LINE = "%s v%d" % (PROTOCOL_NAME, PROTOCOL_VERSION)
DISCOVERY_PORT = 55411
DEFAULT_TCP_PORT = 8899
SERVICE_UUID = "7d3f9c2a-4b8e-4f6a-9c1d-2e5a8b7f0d31"
SERVER_NAME = "Smartphone ReloadAtlas"


# ============================================================================
# Generation d'images
# ============================================================================
class AndroidCamera:
    """Camera Android via pyjnius (API Camera + YuvImage, compression native).

    Fournit start()/stop() et une file de frames JPEG. Le rappel de
    previsualisation arrive sur un thread Java : il ne fait qu'empiler la
    trame compressee dans la file.
    """

    def __init__(self, camera_id, width, height, quality, fps):
        from jnius import autoclass, PythonJavaClass, java_method
        self._autoclass = autoclass
        self.camera_id = int(camera_id)
        self.width, self.height = int(width), int(height)
        self.quality = int(quality)
        self.fps = float(fps)
        self.frames = queue.Queue(maxsize=4)

        Camera = autoclass("android.hardware.Camera")
        ImageFormat = autoclass("android.graphics.ImageFormat")

        class PreviewCallback(PythonJavaClass):
            __javainterfaces__ = ["android/hardware/Camera$PreviewCallback"]

            def __init__(self, owner):
                super().__init__()
                self.owner = owner

            @java_method("(Landroid/hardware/Camera;[B)V")
            def onPreviewFrame(self, camera, data):
                owner = self.owner
                try:
                    jpeg = owner._compress(bytes(data), owner.real_width,
                                           owner.real_height)
                    if jpeg:
                        try:
                            owner.frames.put_nowait(jpeg)
                        except Exception:
                            pass  # file pleine : on saute une image
                except Exception as exc:
                    print("frame:", exc)

        self._PreviewCallback = PreviewCallback
        self._ImageFormat = ImageFormat
        self._camera = None
        self.real_width, self.real_height = self.width, self.height

    def _compress(self, nv21, width, height):
        YuvImage = self._autoclass("android.graphics.YuvImage")
        Rect = self._autoclass("android.graphics.Rect")
        ByteArrayOutputStream = self._autoclass("java.io.ByteArrayOutputStream")
        ImageFormat = self._ImageFormat
        yuv = YuvImage(nv21, ImageFormat.NV21, width, height)
        out = ByteArrayOutputStream()
        yuv.compressToJpeg(Rect(0, 0, width, height), self.quality, out)
        jpeg = bytes(out.toByteArray())
        out.close()
        return jpeg

    @staticmethod
    def count_cameras():
        from jnius import autoclass
        return int(autoclass("android.hardware.Camera").getNumberOfCameras())

    def start(self):
        from jnius import autoclass
        Camera = autoclass("android.hardware.Camera")
        SurfaceTexture = autoclass("android.graphics.SurfaceTexture")

        self._camera = Camera.open(self.camera_id)
        params = self._camera.getParameters()
        self.real_width, self.real_height = self._choose_size(params)
        params.setPreviewSize(self.real_width, self.real_height)
        params.setPreviewFormat(self._ImageFormat.NV21)
        self._camera.setParameters(params)

        # Surface factice : obligatoire pour recevoir les frames sans ecran.
        self._camera.setPreviewTexture(SurfaceTexture(0))
        self._camera.setPreviewCallback(self._PreviewCallback(self))
        self._camera.startPreview()
        print("caméra %d ouverte : %dx%d" % (self.camera_id,
                                             self.real_width,
                                             self.real_height))

    def _choose_size(self, params):
        target = self.width * self.height
        best, best_diff = (self.width, self.height), None
        try:
            for size in params.getSupportedPreviewSizes():
                diff = abs(size.width * size.height - target)
                if best_diff is None or diff < best_diff:
                    best, best_diff = (size.width, size.height), diff
        except Exception:
            pass
        return best

    def stop(self):
        if self._camera is not None:
            try:
                self._camera.setPreviewCallback(None)
                self._camera.stopPreview()
                self._camera.release()
            finally:
                self._camera = None

    def apply_settings(self, quality=None, size=None, fps=None):
        if quality:
            self.quality = max(20, min(95, int(quality)))
        if fps:
            self.fps = max(1.0, min(30.0, float(fps)))
        if size:
            try:
                w, h = size.lower().split("x")
                self.width, self.height = int(w), int(h)
                if self._camera is not None:
                    self.stop()
                    self.start()
            except ValueError:
                pass


class SyntheticCamera:
    """Frames de test (PC ou telephone sans camera) : JPEG via Pillow,
    sinon PPM pur Python — QImage decode les deux."""

    def __init__(self, width=320, height=240, quality=70, fps=8.0):
        self.width, self.height = int(width), int(height)
        self.quality, self.fps = int(quality), float(fps)
        self.frames = queue.Queue(maxsize=4)
        self._seq = 0
        self._running = False
        self._thread = None
        try:
            from PIL import Image, ImageDraw  # noqa: F401
            self.fmt = "jpeg"
        except ImportError:
            self.fmt = "ppm"

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread = None

    def apply_settings(self, quality=None, size=None, fps=None):
        if quality:
            self.quality = int(quality)
        if fps:
            self.fps = float(fps)
        if size:
            try:
                w, h = size.lower().split("x")
                self.width, self.height = int(w), int(h)
            except ValueError:
                pass

    def _run(self):
        while self._running:
            self._seq += 1
            data = self._make_frame(self._seq)
            try:
                self.frames.put_nowait(data)
            except Exception:
                pass
            time.sleep(max(0.05, 1.0 / self.fps))

    def _make_frame(self, seq):
        if self.fmt == "jpeg":
            import io
            from PIL import Image, ImageDraw
            img = Image.new("RGB", (self.width, self.height), (24, 24, 20))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, self.width - 1, self.height - 1],
                           outline=(120, 105, 80), width=3)
            draw.text((8, 8), "SELF-TEST %06d" % seq, fill=(230, 220, 190))
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=self.quality)
            return out.getvalue()
        row = bytearray()
        for x in range(self.width):
            row += bytes((((x + seq) * 5) % 256, 90, 60))
        rows = bytearray(b"P6\n%d %d\n255\n" % (self.width, self.height))
        for _ in range(self.height):
            rows += row
        return bytes(rows)


# ============================================================================
# Session client (TCP natif ou flux Java Bluetooth)
# ============================================================================
def _to_jbytes(data):
    """bytes -> byte[] Java (pyjnius), via String ISO-8859-1."""
    from jnius import autoclass
    JavaString = autoclass("java.lang.String")
    return JavaString(data.decode("latin-1"), "ISO-8859-1").getBytes("ISO-8859-1")


class ClientSession:
    """Poignee de main + boucle d'envoi + lecture des commandes."""

    def __init__(self, camera, reader, writer, closer, label):
        self.camera = camera
        self._reader = reader        # callable -> bytes lus (peut lever)
        self._writer = writer        # callable(bytes) -> ecrit
        self._closer = closer
        self.label = label

    def send_line(self, text):
        self._writer((text + "\n").encode("ascii"))

    def serve(self):
        fmt = getattr(self.camera, "fmt", "jpeg")
        self.send_line(HANDSHAKE_LINE)
        self.send_line("INFO " + json.dumps({
            "name": SERVER_NAME, "fmt": fmt,
            "width": getattr(self.camera, "width", 0),
            "height": getattr(self.camera, "height", 0),
            "fps": getattr(self.camera, "fps", 0),
        }, separators=(",", ":")))
        commands = threading.Thread(target=self._command_loop, daemon=True)
        commands.start()
        print("client connecté (%s) — flux en cours" % self.label)
        try:
            while True:
                jpeg = self.camera.frames.get(timeout=10.0)
                self._writer(("FRAME %d\n" % len(jpeg)).encode("ascii"))
                self._writer(jpeg)
        except Exception as exc:
            print("client déconnecté (%s) : %s" % (self.label, exc))
        finally:
            try:
                self._closer()
            except Exception:
                pass

    def _command_loop(self):
        buffer = b""
        try:
            while True:
                chunk = self._reader()
                if not chunk:
                    return
                buffer += chunk
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    self._handle(line.decode("ascii", "replace").strip())
        except Exception:
            return

    def _handle(self, line):
        if line.startswith("SET "):
            try:
                key, value = line[4:].split("=", 1)
            except ValueError:
                return
            if key == "quality":
                self.camera.apply_settings(quality=value)
            elif key == "size":
                self.camera.apply_settings(size=value)
            elif key == "fps":
                self.camera.apply_settings(fps=value)
        elif line == "PING":
            self.send_line("PONG %d" % int(time.time() * 1000))


# ============================================================================
# Serveurs
# ============================================================================
class DiscoveryResponder(threading.Thread):
    """Repond aux sondes UDP du PC (decouverte automatique)."""

    daemon = True

    def __init__(self, tcp_port):
        super().__init__(name="discovery")
        self.tcp_port = tcp_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._sock.bind(("", DISCOVERY_PORT))
        except OSError as exc:
            print("découverte UDP indisponible :", exc)

    def run(self):
        probe = ("RA-CAM-DISCOVER v%d" % PROTOCOL_VERSION).encode("ascii")
        while True:
            try:
                data, peer = self._sock.recvfrom(512)
                if data.strip() == probe:
                    reply = ("RA-CAM-HERE v%d %d %s"
                             % (PROTOCOL_VERSION, self.tcp_port,
                                SERVER_NAME)).encode("ascii")
                    self._sock.sendto(reply, peer)
            except OSError:
                return


def local_addresses():
    """Adresses IP du telephone/PC, affichees a l'ecran."""
    addresses = []
    try:
        info = socket.gethostbyname_ex(socket.gethostname())
        addresses.extend(info[2])
    except OSError:
        pass
    probe = None
    try:
        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        probe.connect(("10.255.255.255", 1))
        addresses.append(probe.getsockname()[0])
    except OSError:
        pass
    finally:
        if probe:
            probe.close()
    return [a for a in addresses if not a.startswith("127.")]


def serve_tcp(camera, port):
    responder = DiscoveryResponder(port)
    responder.start()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(1)
    addresses = local_addresses()
    first = addresses[0] if addresses else "?"
    print("=" * 60)
    print("LE TÉLÉPHONE FILME ✅  — le serveur est actif.")
    print("NE FERMEZ PAS cette application. Gardez l'écran allumé.")
    print()
    print("Maintenant, sur le PC :")
    print("  1. lancez la fenêtre de test (TestConnexionSmartphone.exe)")
    print("  2. cliquez sur « Détecter »   (aucune adresse à taper)")
    print("  3. cliquez sur « Se connecter » puis « Autoriser »")
    print()
    print("Si « Détecter » ne trouve rien : activez le Point d'accès")
    print("mobile du téléphone, connectez le PC dessus, puis réessayez.")
    print("(Indication technique : %s — port %d)" % (first, port))
    print("=" * 60)
    while True:
        client, peer = server.accept()
        camera.start()

        def reader():
            return client.recv(4096)

        session = ClientSession(camera, reader, client.sendall,
                                client.close, "TCP %s:%d" % peer)
        try:
            session.serve()
        finally:
            camera.stop()


def serve_bluetooth(camera):
    from jnius import autoclass
    BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
    UUID = autoclass("java.util.UUID")
    adapter = BluetoothAdapter.getDefaultAdapter()
    if adapter is None:
        raise SystemExit("Ce téléphone n'a pas de Bluetooth.")
    if not adapter.isEnabled():
        raise SystemExit("Activez le Bluetooth du téléphone (et l'appairage "
                         "depuis les paramètres Windows), puis relancez.")
    server = adapter.listenUsingRfcommWithServiceRecord(
        "ReloadAtlas Camera", UUID.fromString(SERVICE_UUID))
    print("=" * 60)
    print("LE TÉLÉPHONE FILME ✅  — le serveur Bluetooth est actif.")
    print("NE FERMEZ PAS cette application.")
    print("Sur le PC : source « Bluetooth », collez l'adresse MAC du")
    print("téléphone (Paramètres Windows → Bluetooth → appareil appairé),")
    print("puis « Se connecter » → « Autoriser ».")
    print("=" * 60)
    try:
        while True:
            client = server.accept(600000)  # ms
            if client is None:
                continue
            camera.start()
            input_stream = client.getInputStream()
            output_stream = client.getOutputStream()

            def reader():
                return _read_byte(input_stream)

            def writer(data):
                output_stream.write(_to_jbytes(data))
                output_stream.flush()

            def closer():
                client.close()

            session = ClientSession(camera, reader, writer, closer, "Bluetooth")
            try:
                session.serve()
            finally:
                camera.stop()
    finally:
        try:
            server.close()
        except Exception:
            pass


def _read_byte(input_stream):
    """Lit un octet du flux Java (-1 = fin) — lecture lente mais suffisante
    pour les rares commandes du PC."""
    byte = input_stream.read()
    if byte < 0:
        return b""
    return bytes([byte])


def on_android():
    """Detection Android SANS importer pyjnius (l'import peut echouer selon
    le mode de lancement de Pydroid : voir _explain_camera_unavailable)."""
    return hasattr(sys, "getandroidapilevel")


def _explain_camera_unavailable(exc):
    """Message explicatif quand l'acces camera/Java est refuse (cas reel
    rencontre : script lance depuis le mode Terminal de Pydroid 3, ou le
    sous-process n'a pas de machine Java -> pyjnius leve
    'No JNIEnv available in Terminal')."""
    print("=" * 60)
    print("ACCÈS CAMÉRA INDISPONIBLE")
    print("Détail technique : %s" % exc)
    print()
    print("Cause la plus fréquente : le script a été lancé depuis le mode")
    print("« Terminal » de Pydroid, qui n'a pas accès à la caméra.")
    print()
    print("SOLUTION : fermez, puis relancez avec le GROS BOUTON ▶ (triangle)")
    print("de Pydroid 3 — pas depuis un terminal ni l'option « run in")
    print("terminal ». Répondez à nouveau 1 puis 1 aux questions.")
    print()
    print("En attendant, ce compagnon diffuse des IMAGES DE TEST : la")
    print("liaison avec le PC reste testable (Détecter → Se connecter),")
    print("mais l'image n'est PAS celle de la caméra.")
    print("=" * 60)


# ============================================================================
# Point d'entree
# ============================================================================
def _menu():
    """Mode interactif sans arguments — pense aux utilisateurs non techniques.

    Lance depuis Pydroid 3 par un simple appui sur ▶ : petit menu texte,
    reponses par defaut validables avec la touche Entree.
    """
    print("=" * 60)
    print("COMPAGNON RELOADATLAS — caméra du smartphone vers le PC")
    print("=" * 60)
    print("  1. WiFi  (conseillé : point d'accès mobile ou box)")
    print("  2. Bluetooth")
    mode = (input("Votre choix (1 ou 2) ? [1] ").strip() or "1")
    mode = "bt" if mode == "2" else "tcp"
    cam = input("Caméra : 1 = arrière, 2 = avant ? [1] ").strip()
    camera_id = 1 if cam == "2" else 0

    class _Settings:
        pass
    settings = _Settings()
    settings.mode = mode
    settings.camera_id = camera_id
    settings.port = DEFAULT_TCP_PORT
    settings.size = "320x240"
    settings.quality = 60
    settings.fps = 5.0 if mode == "bt" else 12.0
    settings.list_cameras = False
    return settings


def main():
    if len(sys.argv) == 1:
        args = _menu()                     # lancement simple : menu interactif
    else:
        parser = argparse.ArgumentParser(
            description="Compagnon ReloadAtlas : caméra du smartphone vers le PC.")
        parser.add_argument("mode", nargs="?", default="tcp",
                            choices=["tcp", "bt", "selftest"],
                            help="tcp = WiFi, bt = Bluetooth, selftest = test PC")
        parser.add_argument("--port", type=int, default=DEFAULT_TCP_PORT)
        parser.add_argument("--fps", type=float, default=8.0)
        parser.add_argument("--size", default="320x240")
        parser.add_argument("--quality", type=int, default=60)
        parser.add_argument("--camera-id", type=int, default=0)
        parser.add_argument("--list-cameras", action="store_true")
        args = parser.parse_args()

    width, height = (int(v) for v in args.size.lower().split("x"))

    if args.list_cameras:
        if on_android():
            try:
                print("Caméras disponibles :", AndroidCamera.count_cameras())
            except Exception as exc:
                _explain_camera_unavailable(exc)
        else:
            print("Pas sur Android : --list-cameras inutile en selftest.")
        return

    if not on_android():
        camera = SyntheticCamera(width, height, args.quality, args.fps)
        print("MODE SELF-TEST : frames synthétiques (%s)." % camera.fmt)
        serve_tcp(camera, args.port)
        return

    if args.mode == "bt":
        try:
            camera = AndroidCamera(args.camera_id, width, height,
                                   args.quality, args.fps)
            serve_bluetooth(camera)
        except Exception as exc:
            _explain_camera_unavailable(exc)
            print("Le mode Bluetooth ne peut pas fonctionner sans accès Java.")
        return

    try:
        camera = AndroidCamera(args.camera_id, width, height,
                               args.quality, args.fps)
    except Exception as exc:
        _explain_camera_unavailable(exc)
        camera = SyntheticCamera(width, height, args.quality, args.fps)
        print("Bascule automatique en IMAGES DE TEST (voir ci-dessus).")
    serve_tcp(camera, args.port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt du compagnon.")
