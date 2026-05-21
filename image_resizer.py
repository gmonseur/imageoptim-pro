import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import threading
import webbrowser

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageOptim Pro - Redimensionneur & Compresseur")
        self.root.geometry("1000x920")
        self.root.minsize(900, 870)
        
        # Couleurs du thème dark moderne
        self.bg_dark = "#2b2b2b"
        self.bg_medium = "#3a3a3a"
        self.bg_light = "#4a4a4a"
        self.bg_input = "#353535"
        self.fg_primary = "#ffffff"
        self.fg_secondary = "#b0b0b0"
        self.accent_green = "#4caf50"
        self.accent_blue = "#2196f3"
        self.border_color = "#505050"
        
        # Configurer le thème
        self.root.configure(bg=self.bg_dark)
        self.configure_styles()
        
        # Variables
        self.dossier_source = tk.StringVar()
        self.dossier_destination = tk.StringVar()
        self.largeur_max = tk.IntVar(value=2000)
        self.qualite = tk.IntVar(value=85)
        self.conserver_ratio = tk.BooleanVar(value=True)
        self.format_sortie = tk.StringVar(value="original")
        
        # Interface
        self.creer_interface()
        
    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style pour les frames
        style.configure('Dark.TFrame', background=self.bg_dark)
        
        # Style pour les labels
        style.configure('Dark.TLabel', 
                       background=self.bg_dark, 
                       foreground=self.fg_primary)
        
        # Style pour les Entry
        style.configure('Dark.TEntry',
                       fieldbackground=self.bg_input,
                       foreground=self.fg_primary,
                       bordercolor=self.border_color,
                       borderwidth=1,
                       insertcolor=self.fg_primary,
                       relief='solid')
        style.map('Dark.TEntry',
                 fieldbackground=[('focus', self.bg_light)])
        
        # Style pour les Buttons
        style.configure('Dark.TButton',
                       background=self.bg_light,
                       foreground=self.fg_primary,
                       bordercolor=self.border_color,
                       borderwidth=1,
                       relief='solid')
        style.map('Dark.TButton',
                 background=[('active', self.bg_medium)])
        
        # Style pour les Checkbuttons
        style.configure('Dark.TCheckbutton',
                       background=self.bg_dark,
                       foreground=self.fg_primary)
        
        # Style pour les Radiobuttons
        style.configure('Dark.TRadiobutton',
                       background=self.bg_dark,
                       foreground=self.fg_primary)
        
        # Style pour les Progressbar
        style.configure('Green.Horizontal.TProgressbar',
                       background=self.accent_green,
                       troughcolor=self.bg_light,
                       bordercolor=self.border_color,
                       borderwidth=1,
                       lightcolor=self.accent_green,
                       darkcolor=self.accent_green)
        
    def create_section_frame(self, parent, title, icon):
        """Crée une section avec bordure arrondie et titre"""
        # Frame conteneur avec bordure
        container = tk.Frame(parent, bg=self.border_color, padx=1, pady=1)
        
        # Frame intérieur
        frame = tk.Frame(container, bg=self.bg_medium, padx=15, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre de la section
        title_label = tk.Label(frame, text=f"{icon} {title}", 
                              font=("Arial", 10, "bold"),
                              fg=self.fg_primary, bg=self.bg_medium,
                              anchor='w')
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        return container, frame
        
    def open_website(self, event):
        """Ouvre le site web dans le navigateur"""
        webbrowser.open("https://www.gmonseur.be")
        
    def creer_interface(self):
        # Frame principal avec padding
        main_frame = tk.Frame(self.root, bg=self.bg_dark, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre principal
        titre = tk.Label(main_frame, text="🖼️ ImageOptim Pro", 
                        font=("Arial", 20, "bold"), 
                        fg=self.fg_primary, bg=self.bg_dark)
        titre.pack(pady=(0, 5))
        
        sous_titre = tk.Label(main_frame, text="Redimensionnez et compressez vos images par lot", 
                             font=("Arial", 10), 
                             fg=self.fg_secondary, bg=self.bg_dark)
        sous_titre.pack(pady=(0, 20))
        
        # Section 1: Dossiers
        section1_container, section1 = self.create_section_frame(main_frame, "Dossiers", "📁")
        section1_container.pack(fill=tk.X, pady=(0, 15))
        
        # Dossier source
        source_frame = tk.Frame(section1, bg=self.bg_medium)
        source_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(source_frame, text="Dossier source:", 
                font=("Arial", 9), width=18,
                fg=self.fg_primary, bg=self.bg_medium, anchor='w').pack(side=tk.LEFT)
        
        source_entry_frame = tk.Frame(source_frame, bg=self.bg_input, highlightbackground=self.border_color, 
                                     highlightthickness=1)
        source_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        source_entry = tk.Entry(source_entry_frame, textvariable=self.dossier_source,
                               bg=self.bg_input, fg=self.fg_primary,
                               insertbackground=self.fg_primary, relief='flat',
                               font=("Arial", 9), borderwidth=0)
        source_entry.pack(fill=tk.X, padx=8, pady=6)
        
        btn_source = tk.Button(source_frame, text="📂 Parcourir", 
                              command=self.choisir_source,
                              bg=self.bg_light, fg=self.fg_primary,
                              font=("Arial", 9),
                              relief='flat', borderwidth=0,
                              padx=15, pady=6, cursor="hand2")
        btn_source.pack(side=tk.LEFT)
        btn_source.bind("<Enter>", lambda e: btn_source.configure(bg=self.bg_input))
        btn_source.bind("<Leave>", lambda e: btn_source.configure(bg=self.bg_light))
        
        # Dossier destination
        dest_frame = tk.Frame(section1, bg=self.bg_medium)
        dest_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(dest_frame, text="Dossier destination:", 
                font=("Arial", 9), width=18,
                fg=self.fg_primary, bg=self.bg_medium, anchor='w').pack(side=tk.LEFT)
        
        dest_entry_frame = tk.Frame(dest_frame, bg=self.bg_input, highlightbackground=self.border_color, 
                                   highlightthickness=1)
        dest_entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        dest_entry = tk.Entry(dest_entry_frame, textvariable=self.dossier_destination,
                             bg=self.bg_input, fg=self.fg_primary,
                             insertbackground=self.fg_primary, relief='flat',
                             font=("Arial", 9), borderwidth=0)
        dest_entry.pack(fill=tk.X, padx=8, pady=6)
        
        btn_dest = tk.Button(dest_frame, text="📂 Parcourir", 
                            command=self.choisir_destination,
                            bg=self.bg_light, fg=self.fg_primary,
                            font=("Arial", 9),
                            relief='flat', borderwidth=0,
                            padx=15, pady=6, cursor="hand2")
        btn_dest.pack(side=tk.LEFT)
        btn_dest.bind("<Enter>", lambda e: btn_dest.configure(bg=self.bg_input))
        btn_dest.bind("<Leave>", lambda e: btn_dest.configure(bg=self.bg_light))
        
        # Section 2: Redimensionnement
        section2_container, section2 = self.create_section_frame(main_frame, "Redimensionnement", "📏")
        section2_container.pack(fill=tk.X, pady=(0, 15))
        
        largeur_frame = tk.Frame(section2, bg=self.bg_medium)
        largeur_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(largeur_frame, text="Largeur maximale:", 
                font=("Arial", 9),
                fg=self.fg_primary, bg=self.bg_medium).pack(side=tk.LEFT)
        
        largeur_entry_frame = tk.Frame(largeur_frame, bg=self.bg_input, highlightbackground=self.border_color, 
                                      highlightthickness=1)
        largeur_entry_frame.pack(side=tk.LEFT, padx=10)
        
        largeur_entry = tk.Entry(largeur_entry_frame, textvariable=self.largeur_max, width=8,
                                bg=self.bg_input, fg=self.fg_primary,
                                insertbackground=self.fg_primary, relief='flat',
                                font=("Arial", 9), borderwidth=0, justify='center')
        largeur_entry.pack(padx=8, pady=6)
        
        tk.Label(largeur_frame, text="pixels", 
                fg=self.fg_primary, bg=self.bg_medium,
                font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Checkbox avec style custom
        check_frame = tk.Frame(largeur_frame, bg=self.bg_medium)
        check_frame.pack(side=tk.LEFT, padx=20)
        
        self.check_var = tk.IntVar(value=1)
        check = tk.Checkbutton(check_frame, text="Conserver les proportions",
                              variable=self.check_var,
                              bg=self.bg_medium, fg=self.fg_primary,
                              selectcolor=self.bg_light,
                              activebackground=self.bg_medium,
                              activeforeground=self.fg_primary,
                              font=("Arial", 9),
                              borderwidth=0, highlightthickness=0)
        check.pack()
        
        # Section 3: Compression
        section3_container, section3 = self.create_section_frame(main_frame, "Compression", "🗜️")
        section3_container.pack(fill=tk.X, pady=(0, 15))
        
        # Qualité
        qualite_label_frame = tk.Frame(section3, bg=self.bg_medium)
        qualite_label_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(qualite_label_frame, text="Qualité de compression:", 
                font=("Arial", 9),
                fg=self.fg_primary, bg=self.bg_medium).pack(side=tk.LEFT)
        
        self.qualite_value = tk.Label(qualite_label_frame, text=f"{self.qualite.get()}%", 
                                     font=("Arial", 9, "bold"), 
                                     fg=self.accent_green, bg=self.bg_medium)
        self.qualite_value.pack(side=tk.RIGHT)
        
        # Slider
        slider_frame = tk.Frame(section3, bg=self.bg_medium)
        slider_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(slider_frame, text="Faible\n(petit fichier)", 
                font=("Arial", 7), 
                fg=self.fg_secondary, bg=self.bg_medium).pack(side=tk.LEFT, padx=(0, 5))
        
        # Slider custom
        slider_bg = tk.Frame(slider_frame, bg=self.bg_light, height=6)
        slider_bg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.slider = tk.Scale(slider_bg, from_=10, to=100, orient=tk.HORIZONTAL,
                              variable=self.qualite, command=self.update_qualite_label,
                              bg=self.bg_light, fg=self.fg_primary,
                              troughcolor=self.bg_input,
                              activebackground=self.accent_green,
                              highlightthickness=0, borderwidth=0,
                              sliderrelief='flat', width=15, length=400)
        self.slider.pack(fill=tk.X)
        
        tk.Label(slider_frame, text="Élevée\n(gros fichier)", 
                font=("Arial", 7), 
                fg=self.fg_secondary, bg=self.bg_medium).pack(side=tk.LEFT, padx=(5, 0))
        
        # Format de sortie
        format_frame = tk.Frame(section3, bg=self.bg_medium)
        format_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(format_frame, text="Format de sortie:", 
                font=("Arial", 9),
                fg=self.fg_primary, bg=self.bg_medium).pack(side=tk.LEFT, padx=(0, 15))
        
        formats = [("Conserver l'original", "original"), 
                   ("JPEG", "jpeg"), 
                   ("PNG", "png"), 
                   ("WebP (recommandé)", "webp")]
        
        for text, value in formats:
            rb = tk.Radiobutton(format_frame, text=text, variable=self.format_sortie, 
                               value=value, bg=self.bg_medium, fg=self.fg_primary,
                               selectcolor=self.bg_light,
                               activebackground=self.bg_medium,
                               activeforeground=self.fg_primary,
                               font=("Arial", 9),
                               borderwidth=0, highlightthickness=0)
            rb.pack(side=tk.LEFT, padx=10)
        
        # Barre de progression
        progress_frame = tk.Frame(main_frame, bg=self.bg_dark)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_label = tk.Label(progress_frame, text="Prêt", 
                                      font=("Arial", 9),
                                      fg=self.fg_secondary, bg=self.bg_dark)
        self.progress_label.pack()
        
        # Progress bar avec bordure
        progress_border = tk.Frame(progress_frame, bg=self.border_color, height=24)
        progress_border.pack(fill=tk.X, pady=5, padx=1)
        
        self.progress = ttk.Progressbar(progress_border, mode='determinate', 
                                       style='Green.Horizontal.TProgressbar')
        self.progress.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Section Logs
        log_container, log_section = self.create_section_frame(main_frame, "Journal (Logs)", "📋")
        log_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Zone de texte
        text_border = tk.Frame(log_section, bg=self.border_color)
        text_border.pack(fill=tk.BOTH, expand=True)
        
        log_scroll_frame = tk.Frame(text_border, bg=self.bg_input)
        log_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        scrollbar = tk.Scrollbar(log_scroll_frame, bg=self.bg_light)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_scroll_frame, height=8, 
                               yscrollcommand=scrollbar.set, 
                               font=("Courier", 9),
                               bg=self.bg_input, fg=self.fg_primary,
                               insertbackground=self.fg_primary,
                               selectbackground=self.accent_green,
                               selectforeground=self.fg_primary,
                               borderwidth=0, highlightthickness=0,
                               relief='flat', padx=10, pady=10)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Boutons
        btn_frame = tk.Frame(main_frame, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Bouton démarrer
        self.btn_demarrer = tk.Button(btn_frame, text="🚀 Démarrer le traitement", 
                                      command=self.demarrer_traitement,
                                      font=("Arial", 11, "bold"), 
                                      bg=self.accent_green, fg="#ffffff",
                                      activebackground="#66bb6a",
                                      activeforeground="#ffffff",
                                      padx=40, pady=15, cursor="hand2",
                                      borderwidth=0, highlightthickness=0,
                                      relief=tk.FLAT)
        self.btn_demarrer.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        self.btn_demarrer.bind("<Enter>", lambda e: self.btn_demarrer.configure(bg="#66bb6a"))
        self.btn_demarrer.bind("<Leave>", lambda e: self.btn_demarrer.configure(bg=self.accent_green))
        
        # Bouton effacer
        btn_effacer = tk.Button(btn_frame, text="🗑️ Effacer les logs", 
                               command=self.effacer_logs,
                               font=("Arial", 10), 
                               bg=self.bg_light, fg=self.fg_primary,
                               activebackground=self.bg_medium,
                               activeforeground=self.fg_primary,
                               padx=20, pady=15, cursor="hand2",
                               borderwidth=0, highlightthickness=0,
                               relief=tk.FLAT)
        btn_effacer.pack(side=tk.LEFT)
        
        btn_effacer.bind("<Enter>", lambda e: btn_effacer.configure(bg=self.bg_medium))
        btn_effacer.bind("<Leave>", lambda e: btn_effacer.configure(bg=self.bg_light))
        
        # Crédit en bas avec lien cliquable
        credit_frame = tk.Frame(main_frame, bg=self.bg_dark)
        credit_frame.pack(fill=tk.X, pady=(5, 0))
        
        credit = tk.Label(credit_frame, text="Développé par www.gmonseur.be", 
                         font=("Arial", 9), 
                         fg=self.accent_blue, bg=self.bg_dark,
                         cursor="hand2")
        credit.pack()
        
        # Rendre le lien cliquable
        credit.bind("<Button-1>", self.open_website)
        credit.bind("<Enter>", lambda e: credit.configure(fg="#64b5f6"))
        credit.bind("<Leave>", lambda e: credit.configure(fg=self.accent_blue))
        
    def update_qualite_label(self, value):
        qualite = int(float(value))
        self.qualite_value.config(text=f"{qualite}%")
        
        if qualite < 50:
            color = "#f44336"
        elif qualite < 75:
            color = "#ff9800"
        else:
            color = self.accent_green
        
        self.qualite_value.config(foreground=color)
        
    def choisir_source(self):
        dossier = filedialog.askdirectory(title="Choisir le dossier source")
        if dossier:
            self.dossier_source.set(dossier)
            self.log(f"📂 Dossier source: {dossier}")
            
    def choisir_destination(self):
        dossier = filedialog.askdirectory(title="Choisir le dossier de destination")
        if dossier:
            self.dossier_destination.set(dossier)
            self.log(f"📂 Dossier destination: {dossier}")
            
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def effacer_logs(self):
        self.log_text.delete(1.0, tk.END)
        
    def get_extension(self, format_sortie, original_ext):
        if format_sortie == "original":
            return original_ext
        elif format_sortie == "jpeg":
            return ".jpg"
        elif format_sortie == "png":
            return ".png"
        elif format_sortie == "webp":
            return ".webp"
        return original_ext
        
    def redimensionner_images(self):
        dossier_source = self.dossier_source.get()
        dossier_destination = self.dossier_destination.get()
        largeur_max = self.largeur_max.get()
        qualite = self.qualite.get()
        format_sortie = self.format_sortie.get()
        
        if not dossier_source or not dossier_destination:
            messagebox.showerror("Erreur", "Veuillez sélectionner les dossiers source et destination")
            self.btn_demarrer.config(state=tk.NORMAL)
            return
            
        if not os.path.exists(dossier_source):
            messagebox.showerror("Erreur", "Le dossier source n'existe pas")
            self.btn_demarrer.config(state=tk.NORMAL)
            return
        
        if not os.path.exists(dossier_destination):
            os.makedirs(dossier_destination)
        
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.JPEG', '.PNG', '.BMP', '.webp', '.WEBP']
        images = [f for f in os.listdir(dossier_source) if any(f.endswith(ext) for ext in extensions)]
        total_images = len(images)
        
        if total_images == 0:
            messagebox.showwarning("Attention", "Aucune image trouvée dans le dossier source")
            self.btn_demarrer.config(state=tk.NORMAL)
            return
        
        self.log(f"\n{'='*60}")
        self.log(f"🎬 DÉBUT DU TRAITEMENT")
        self.log(f"{'='*60}")
        self.log(f"📊 Images à traiter: {total_images}")
        self.log(f"📏 Largeur max: {largeur_max}px | Qualité: {qualite}%")
        self.log(f"{'='*60}\n")
        
        self.progress['maximum'] = total_images
        self.progress['value'] = 0
        
        taille_originale_totale = 0
        taille_finale_totale = 0
        
        for index, filename in enumerate(images):
            chemin_source = os.path.join(dossier_source, filename)
            
            try:
                with Image.open(chemin_source) as img:
                    if img.mode in ('RGBA', 'LA', 'P') and format_sortie == 'jpeg':
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = rgb_img
                    
                    largeur_orig, hauteur_orig = img.size
                    taille_originale = os.path.getsize(chemin_source)
                    taille_originale_totale += taille_originale
                    
                    nom_sans_ext = os.path.splitext(filename)[0]
                    ext_originale = os.path.splitext(filename)[1]
                    nouvelle_ext = self.get_extension(format_sortie, ext_originale)
                    nouveau_nom = nom_sans_ext + nouvelle_ext
                    
                    chemin_destination = os.path.join(dossier_destination, nouveau_nom)
                    
                    if largeur_orig > largeur_max:
                        ratio = largeur_max / float(largeur_orig)
                        nouvelle_hauteur = int(hauteur_orig * ratio)
                        img_redimensionnee = img.resize((largeur_max, nouvelle_hauteur), Image.Resampling.LANCZOS)
                        
                        if nouvelle_ext.lower() in ['.jpg', '.jpeg']:
                            img_redimensionnee.save(chemin_destination, 'JPEG', quality=qualite, optimize=True)
                        elif nouvelle_ext.lower() == '.png':
                            img_redimensionnee.save(chemin_destination, 'PNG', optimize=True)
                        elif nouvelle_ext.lower() == '.webp':
                            img_redimensionnee.save(chemin_destination, 'WEBP', quality=qualite)
                        else:
                            img_redimensionnee.save(chemin_destination, quality=qualite)
                        
                        taille_finale = os.path.getsize(chemin_destination)
                        taille_finale_totale += taille_finale
                        reduction = ((taille_originale - taille_finale) / taille_originale) * 100
                        
                        self.log(f"✅ {filename} | {largeur_orig}x{hauteur_orig}→{largeur_max}x{nouvelle_hauteur} | -{reduction:.0f}%")
                    else:
                        if nouvelle_ext.lower() in ['.jpg', '.jpeg']:
                            img.save(chemin_destination, 'JPEG', quality=qualite, optimize=True)
                        elif nouvelle_ext.lower() == '.png':
                            img.save(chemin_destination, 'PNG', optimize=True)
                        elif nouvelle_ext.lower() == '.webp':
                            img.save(chemin_destination, 'WEBP', quality=qualite)
                        else:
                            img.save(chemin_destination, quality=qualite)
                        
                        taille_finale = os.path.getsize(chemin_destination)
                        taille_finale_totale += taille_finale
                        reduction = ((taille_originale - taille_finale) / taille_originale) * 100
                        
                        self.log(f"✅ {filename} | conservé | -{reduction:.0f}%")
                    
            except Exception as e:
                self.log(f"❌ {filename}: {str(e)}")
            
            self.progress['value'] = index + 1
            self.progress_label.config(text=f"Traitement: {index + 1}/{total_images}")
            self.root.update_idletasks()
        
        reduction_totale = ((taille_originale_totale - taille_finale_totale) / taille_originale_totale) * 100 if taille_originale_totale > 0 else 0
        
        self.log(f"\n{'='*60}")
        self.log(f"🎉 TERMINÉ! {total_images} images | Économie: {reduction_totale:.1f}%")
        self.log(f"{'='*60}\n")
        
        self.progress_label.config(text=f"✅ Terminé!")
        
        messagebox.showinfo("Succès", 
                          f"✅ Traitement terminé!\n\n"
                          f"📊 {total_images} images traitées\n"
                          f"💾 Économie: {reduction_totale:.1f}%")
        
        self.btn_demarrer.config(state=tk.NORMAL)
        
    def demarrer_traitement(self):
        self.effacer_logs()
        self.btn_demarrer.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.redimensionner_images)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
