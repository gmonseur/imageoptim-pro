import asyncio
import flet as ft
from PIL import Image
import os
import webbrowser


def main(page: ft.Page):
    page.title = "ImageOptim Pro - Redimensionneur & Compresseur"
    page.window.width = 1000
    page.window.height = 920
    page.window.min_width = 900
    page.window.min_height = 870
    page.bgcolor = "#2b2b2b"
    page.padding = 20

    # Palette
    BG_DARK      = "#2b2b2b"
    BG_MEDIUM    = "#3a3a3a"
    BG_LIGHT     = "#4a4a4a"
    BG_INPUT     = "#353535"
    FG_PRIMARY   = "#ffffff"
    FG_SECONDARY = "#b0b0b0"
    ACCENT_GREEN = "#4caf50"
    ACCENT_BLUE  = "#2196f3"
    BORDER       = "#505050"

    # ── Champs texte ──────────────────────────────────────────────────────

    txt_source = ft.TextField(
        hint_text="Sélectionnez le dossier source…",
        bgcolor=BG_INPUT, color=FG_PRIMARY,
        border_color=BORDER, expand=True,
        text_size=13, height=42,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=6),
    )

    txt_destination = ft.TextField(
        hint_text="Sélectionnez le dossier de destination…",
        bgcolor=BG_INPUT, color=FG_PRIMARY,
        border_color=BORDER, expand=True,
        text_size=13, height=42,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=6),
    )

    txt_largeur = ft.TextField(
        value="2000",
        bgcolor=BG_INPUT, color=FG_PRIMARY,
        border_color=BORDER, width=100,
        text_size=13, height=42,
        text_align=ft.TextAlign.CENTER,
        content_padding=ft.Padding.symmetric(horizontal=10, vertical=6),
    )

    # ── Options ───────────────────────────────────────────────────────────

    check_proportions = ft.Checkbox(
        label="Conserver les proportions",
        value=True,
        fill_color=ACCENT_GREEN,
        check_color=FG_PRIMARY,
        label_style=ft.TextStyle(color=FG_PRIMARY, size=13),
    )

    qualite_label = ft.Text(
        "85%", color=ACCENT_GREEN,
        weight=ft.FontWeight.BOLD, size=13,
    )

    def on_slider_change(e):
        val = int(e.control.value)
        qualite_label.value = f"{val}%"
        qualite_label.color = (
            "#f44336" if val < 50 else
            "#ff9800" if val < 75 else
            ACCENT_GREEN
        )
        qualite_label.update()

    slider_qualite = ft.Slider(
        min=10, max=100, value=85,
        active_color=ACCENT_GREEN,
        inactive_color=BG_INPUT,
        thumb_color=ACCENT_GREEN,
        on_change=on_slider_change,
        expand=True,
    )

    format_group = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="original", label="Conserver l'original",
                     fill_color=ACCENT_GREEN,
                     label_style=ft.TextStyle(color=FG_PRIMARY, size=13)),
            ft.Radio(value="jpeg", label="JPEG",
                     fill_color=ACCENT_GREEN,
                     label_style=ft.TextStyle(color=FG_PRIMARY, size=13)),
            ft.Radio(value="png", label="PNG",
                     fill_color=ACCENT_GREEN,
                     label_style=ft.TextStyle(color=FG_PRIMARY, size=13)),
            ft.Radio(value="webp", label="WebP (recommandé)",
                     fill_color=ACCENT_GREEN,
                     label_style=ft.TextStyle(color=FG_PRIMARY, size=13)),
        ]),
        value="original",
    )

    # ── Progression ───────────────────────────────────────────────────────

    progress_bar = ft.ProgressBar(
        value=0,
        color=ACCENT_GREEN,
        bgcolor=BG_LIGHT,
        expand=True,
        height=18,
    )

    progress_label = ft.Text("Prêt", color=FG_SECONDARY, size=13)

    # ── Journal ───────────────────────────────────────────────────────────

    log_list = ft.ListView(expand=True, auto_scroll=True, spacing=1)

    def add_log(message):
        log_list.controls.append(
            ft.Text(message, color=FG_PRIMARY, size=12,
                    font_family="Courier New", selectable=True)
        )
        page.update()

    def clear_logs(e=None):
        log_list.controls.clear()
        page.update()

    # ── Dialogues ────────────────────────────────────────────────────────

    def show_dialog(title, message):
        dlg = ft.AlertDialog(
            title=ft.Text(title, color=FG_PRIMARY),
            content=ft.Text(message, color=FG_SECONDARY),
            bgcolor=BG_MEDIUM,
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: page.pop_dialog(),
                    style=ft.ButtonStyle(color=ACCENT_GREEN),
                )
            ],
        )
        page.show_dialog(dlg)

    # ── FilePickers (async) ───────────────────────────────────────────────

    source_picker = ft.FilePicker()
    dest_picker   = ft.FilePicker()
    page.services.extend([source_picker, dest_picker])

    async def pick_source(e):
        path = await source_picker.get_directory_path(
            dialog_title="Choisir le dossier source"
        )
        if path:
            txt_source.value = path
            txt_source.update()
            add_log(f"📂 Dossier source: {path}")

    async def pick_dest(e):
        path = await dest_picker.get_directory_path(
            dialog_title="Choisir le dossier de destination"
        )
        if path:
            txt_destination.value = path
            txt_destination.update()
            add_log(f"📂 Dossier destination: {path}")

    # ── Traitement images ─────────────────────────────────────────────────

    def get_extension(format_sortie, original_ext):
        return {"jpeg": ".jpg", "png": ".png", "webp": ".webp"}.get(
            format_sortie, original_ext
        )

    async def redimensionner_images():
        src = txt_source.value or ""
        dst = txt_destination.value or ""
        try:
            largeur_max = int(txt_largeur.value)
        except ValueError:
            largeur_max = 2000
        qualite       = int(slider_qualite.value)
        format_sortie = format_group.value

        if not src or not dst:
            btn_demarrer.disabled = False
            page.update()
            show_dialog("Erreur", "Veuillez sélectionner les dossiers source et destination.")
            return

        if not os.path.exists(src):
            btn_demarrer.disabled = False
            page.update()
            show_dialog("Erreur", "Le dossier source n'existe pas.")
            return

        os.makedirs(dst, exist_ok=True)

        extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
        images = [
            f for f in os.listdir(src)
            if os.path.splitext(f)[1].lower() in extensions
        ]
        total = len(images)

        if total == 0:
            btn_demarrer.disabled = False
            page.update()
            show_dialog("Attention", "Aucune image trouvée dans le dossier source.")
            return

        def _log(msg):
            log_list.controls.append(
                ft.Text(msg, color=FG_PRIMARY, size=12,
                        font_family="Courier New", selectable=True)
            )

        _log(f"\n{'='*60}")
        _log("🎬 DÉBUT DU TRAITEMENT")
        _log(f"{'='*60}")
        _log(f"📊 Images à traiter: {total}")
        _log(f"📏 Largeur max: {largeur_max}px | Qualité: {qualite}%")
        _log(f"{'='*60}\n")
        progress_bar.value = 0
        page.update()

        taille_orig_totale = taille_fin_totale = 0
        completed = 0
        sem = asyncio.Semaphore(min(os.cpu_count() or 4, 8))

        def _process(filename):
            chemin_src = os.path.join(src, filename)
            with Image.open(chemin_src) as img:
                if img.mode in ('RGBA', 'LA', 'P') and format_sortie == 'jpeg':
                    rgb = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb

                w_orig, h_orig = img.size
                t_orig = os.path.getsize(chemin_src)

                nom_base     = os.path.splitext(filename)[0]
                ext_orig     = os.path.splitext(filename)[1]
                nouvelle_ext = get_extension(format_sortie, ext_orig)
                chemin_dst   = os.path.join(dst, nom_base + nouvelle_ext)

                if w_orig > largeur_max:
                    ratio = largeur_max / float(w_orig)
                    h_new = int(h_orig * ratio)
                    img_out   = img.resize((largeur_max, h_new), Image.Resampling.LANCZOS)
                    dim_label = f"{w_orig}x{h_orig}→{largeur_max}x{h_new}"
                else:
                    img_out   = img
                    dim_label = "conservé"

                ext_low = nouvelle_ext.lower()
                if ext_low in ('.jpg', '.jpeg'):
                    img_out.save(chemin_dst, 'JPEG', quality=qualite, optimize=True)
                elif ext_low == '.png':
                    img_out.save(chemin_dst, 'PNG', optimize=True)
                elif ext_low == '.webp':
                    img_out.save(chemin_dst, 'WEBP', quality=qualite)
                else:
                    img_out.save(chemin_dst, quality=qualite)

                t_fin = os.path.getsize(chemin_dst)
                reduction = ((t_orig - t_fin) / t_orig) * 100
                return dim_label, reduction, t_orig, t_fin

        async def _process_and_report(filename):
            nonlocal completed, taille_orig_totale, taille_fin_totale
            async with sem:
                try:
                    dim_label, reduction, t_orig, t_fin = await asyncio.to_thread(_process, filename)
                    taille_orig_totale += t_orig
                    taille_fin_totale  += t_fin
                    _log(f"✅ {filename} | {dim_label} | -{reduction:.0f}%")
                except Exception as exc:
                    _log(f"❌ {filename}: {exc}")
            completed += 1
            progress_bar.value = completed / total
            progress_label.value = f"Traitement: {completed}/{total}"
            page.update()

        await asyncio.gather(*[_process_and_report(f) for f in images])

        eco = (
            ((taille_orig_totale - taille_fin_totale) / taille_orig_totale) * 100
            if taille_orig_totale > 0 else 0
        )
        _log(f"\n{'='*60}")
        _log(f"🎉 TERMINÉ! {total} images | Économie: {eco:.1f}%")
        _log(f"{'='*60}\n")

        progress_label.value = "✅ Terminé!"
        btn_demarrer.disabled = False
        page.update()
        show_dialog(
            "Succès",
            f"✅ Traitement terminé!\n\n📊 {total} images traitées\n💾 Économie: {eco:.1f}%",
        )

    def demarrer_traitement(e):
        clear_logs()
        btn_demarrer.disabled = True
        page.update()
        page.run_task(redimensionner_images)

    # ── Boutons ───────────────────────────────────────────────────────────

    btn_demarrer = ft.Button(
        content=ft.Text("🚀 Démarrer le traitement",
                        size=14, weight=ft.FontWeight.BOLD, color="#ffffff"),
        on_click=demarrer_traitement,
        bgcolor=ACCENT_GREEN,
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=30, vertical=16),
        ),
        expand=True,
    )

    btn_effacer = ft.Button(
        content=ft.Text("🗑️ Effacer les logs", size=13, color=FG_PRIMARY),
        on_click=clear_logs,
        bgcolor=BG_LIGHT,
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
        ),
    )

    btn_src = ft.Button(
        content=ft.Text("📂 Parcourir", color=FG_PRIMARY),
        on_click=pick_source,
        bgcolor=BG_LIGHT,
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        ),
    )

    btn_dst = ft.Button(
        content=ft.Text("📂 Parcourir", color=FG_PRIMARY),
        on_click=pick_dest,
        bgcolor=BG_LIGHT,
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        ),
    )

    # ── Helper mise en page ───────────────────────────────────────────────

    def section(title, icon, content):
        return ft.Container(
            content=ft.Column([
                ft.Text(f"{icon}  {title}",
                        color=FG_PRIMARY,
                        weight=ft.FontWeight.BOLD,
                        size=14),
                ft.Divider(color=BORDER, height=1, thickness=1),
                content,
            ], spacing=10),
            bgcolor=BG_MEDIUM,
            border=ft.Border.all(1, BORDER),
            border_radius=8,
            padding=15,
        )

    # ── Interface ─────────────────────────────────────────────────────────

    layout = ft.Column(
        controls=[
            ft.Text("🖼️ ImageOptim Pro",
                    size=22, weight=ft.FontWeight.BOLD,
                    color=FG_PRIMARY, text_align=ft.TextAlign.CENTER),
            ft.Text("Redimensionnez et compressez vos images par lot",
                    size=11, color=FG_SECONDARY, text_align=ft.TextAlign.CENTER),

            section("Dossiers", "📁", ft.Column([
                ft.Row([
                    ft.Text("Dossier source:",
                            color=FG_PRIMARY, size=13, width=165),
                    txt_source,
                    btn_src,
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("Dossier destination:",
                            color=FG_PRIMARY, size=13, width=165),
                    txt_destination,
                    btn_dst,
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=10)),

            section("Redimensionnement", "📏", ft.Row([
                ft.Text("Largeur maximale:", color=FG_PRIMARY, size=13),
                txt_largeur,
                ft.Text("pixels", color=FG_PRIMARY, size=13),
                ft.Container(width=20),
                check_proportions,
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)),

            section("Compression", "🗜️", ft.Column([
                ft.Row([
                    ft.Text("Qualité de compression:",
                            color=FG_PRIMARY, size=13),
                    ft.Container(expand=True),
                    qualite_label,
                ]),
                ft.Row([
                    ft.Text("Faible\n(petit fichier)",
                            color=FG_SECONDARY, size=10,
                            text_align=ft.TextAlign.CENTER),
                    slider_qualite,
                    ft.Text("Élevée\n(gros fichier)",
                            color=FG_SECONDARY, size=10,
                            text_align=ft.TextAlign.CENTER),
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("Format de sortie:",
                            color=FG_PRIMARY, size=13),
                    format_group,
                ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=12)),

            ft.Column([
                ft.Row([progress_label],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=progress_bar,
                    border=ft.Border.all(1, BORDER),
                    border_radius=4,
                    padding=2,
                ),
            ], spacing=6),

            section("Journal (Logs)", "📋", ft.Container(
                content=log_list,
                bgcolor=BG_INPUT,
                border=ft.Border.all(1, BORDER),
                border_radius=4,
                height=180,
                padding=10,
            )),

            ft.Row([btn_demarrer, btn_effacer], spacing=10),

            ft.Row([
                ft.TextButton(
                    content=ft.Text("Développé par www.gmonseur.be",
                                    color=ACCENT_BLUE),
                    on_click=lambda e: webbrowser.open("https://www.gmonseur.be"),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    ft.run(main)
