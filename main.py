# -*- coding: utf-8 -*-
"""ReloadAtlas Camera — application Android (APK) du compagnon.

Reutilise camera_server_phone.py (meme dossier, empaquete par buildozer).
Interface volontairement minimale : deux gros boutons, un statut clair
pour non-initie, autorisations Android demandees au demarrage.

La camera ne fonctionnera PAS si l'utilisateur refuse l'autorisation :
le statut l'explique alors et l'application bascule en images de test
(la liaison reseau reste verifiable).
"""

import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

import camera_server_phone as companion

STATE = {"text": "", "started": False}

WELCOME = (
    "1. Si Android demande des autorisations\n"
    "    (caméra, Bluetooth), touchez AUTORISER.\n"
    "\n"
    "2. Appuyez sur « Démarrer en WiFi ».\n"
    "\n"
    "3. Sur le PC : bouton « Détecter »\n"
    "    puis « Se connecter ».")


def _request_android_permissions():
    """Demande les autorisations a l'execution (obligatoire Android 6+)."""
    try:
        from android.permissions import Permission, request_permissions
        request_permissions([
            Permission.CAMERA,
            Permission.BLUETOOTH,
            Permission.BLUETOOTH_ADMIN,
            Permission.BLUETOOTH_CONNECT,
            Permission.BLUETOOTH_SCAN,
            Permission.ACCESS_FINE_LOCATION,
        ])
    except Exception:
        pass  # hors APK (test desktop) : rien a demander


class ReloadAtlasCameraApp(App):
    title = "ReloadAtlas Camera"

    def build(self):
        _request_android_permissions()
        layout = BoxLayout(orientation="vertical", padding=16, spacing=12)

        title = Label(text="ReloadAtlas Camera", font_size="24sp", bold=True)
        title.size_hint_y = 0.15
        layout.add_widget(title)

        self.status = Label(text=WELCOME, halign="left", valign="top",
                            font_size="16sp")
        self.status.size_hint_y = 0.55
        layout.add_widget(self.status)

        wifi = Button(text="Démarrer en WiFi\n(conseillé)", font_size="20sp")
        wifi.size_hint_y = 0.15
        wifi.bind(on_press=lambda *_: self._start("tcp"))
        layout.add_widget(wifi)

        bluetooth = Button(text="Démarrer en Bluetooth", font_size="20sp")
        bluetooth.size_hint_y = 0.15
        bluetooth.bind(on_press=lambda *_: self._start("bt"))
        layout.add_widget(bluetooth)

        Clock.schedule_interval(self._refresh, 1.0)
        return layout

    def _start(self, mode):
        if STATE["started"]:
            STATE["text"] = ("Déjà actif — sur le PC : « Détecter » puis "
                             "« Se connecter ».")
            return
        STATE["started"] = True

        def run():
            try:
                if mode == "bt":
                    camera = companion.AndroidCamera(0, 320, 240, 60, 5.0)
                    STATE["text"] = (
                        "LE TÉLÉPHONE FILME ✅ (Bluetooth)\n"
                        "\n"
                        "Sur le PC :\n"
                        "  source « Bluetooth »,\n"
                        "  collez l'adresse MAC du téléphone,\n"
                        "  puis « Se connecter » → « Autoriser ».")
                    companion.serve_bluetooth(camera)
                else:
                    camera = companion.AndroidCamera(0, 320, 240, 60, 12.0)
                    STATE["text"] = "LE TÉLÉPHONE FILME ✅"
                    companion.serve_tcp(camera, companion.DEFAULT_TCP_PORT)
            except Exception as exc:
                STATE["text"] = (
                    "ACCÈS CAMÉRA INDISPONIBLE\n"
                    "(%s)\n"
                    "\n"
                    "Vérifiez : Paramètres → Applications →\n"
                    "ReloadAtlas Camera → Autorisations → Caméra,\n"
                    "puis fermez et rouvrez l'application.\n"
                    "\n"
                    "En attendant : IMAGES DE TEST\n"
                    "(la liaison PC reste testable)." % exc)
                try:
                    camera = companion.SyntheticCamera(320, 240, 70, 12.0)
                    companion.serve_tcp(camera, companion.DEFAULT_TCP_PORT)
                except Exception:
                    pass

        threading.Thread(target=run, daemon=True).start()

    def _refresh(self, *_):
        text = STATE["text"]
        if text.startswith("LE TÉLÉPHONE FILME") and "Bluetooth" not in text:
            addresses = ", ".join(companion.local_addresses()) or "?"
            text += ("\n\nSur le PC : « Détecter » puis « Se connecter ».\n"
                     "Adresse : %s — port %d"
                     % (addresses, companion.DEFAULT_TCP_PORT))
        if text and text != self.status.text:
            self.status.text = text


if __name__ == "__main__":
    ReloadAtlasCameraApp().run()
