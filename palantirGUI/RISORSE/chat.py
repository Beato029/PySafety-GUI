import json
import pickle
import sqlite3
import os
import threading
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ==================== CLASSI CORE ====================

class Message:
    def __init__(self, sender: str, content: str, timestamp: datetime = None):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            sender=data['sender'],
            content=data['content'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M')}] {self.sender}: {self.content}"

class Chat:
    def __init__(self, chat_id: str, participants: List[str]):
        self.chat_id = chat_id
        self.participants = participants
        self.messages: List[Message] = []
    
    def add_message(self, message: Message):
        self.messages.append(message)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'chat_id': self.chat_id,
            'participants': self.participants,
            'messages': [msg.to_dict() for msg in self.messages]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        chat = cls(data['chat_id'], data['participants'])
        chat.messages = [Message.from_dict(msg) for msg in data['messages']]
        return chat

# ==================== GESTIONE DATABASE ====================

class ChatDatabase:
    def __init__(self, db_path: str = "chats.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inizializza il database e le tabelle"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id TEXT PRIMARY KEY,
                    participants TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT,
                    sender TEXT,
                    content TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
                )
            ''')
    
    def save_chat(self, chat: Chat):
        """Salva una chat nel database"""
        with sqlite3.connect(self.db_path) as conn:
            # Salva la chat
            conn.execute(
                'INSERT OR REPLACE INTO chats (chat_id, participants) VALUES (?, ?)',
                (chat.chat_id, json.dumps(chat.participants))
            )
            
            # Cancella messaggi esistenti e salva nuovi
            conn.execute('DELETE FROM messages WHERE chat_id = ?', (chat.chat_id,))
            
            for message in chat.messages:
                conn.execute(
                    '''INSERT INTO messages (chat_id, sender, content, timestamp)
                       VALUES (?, ?, ?, ?)''',
                    (chat.chat_id, message.sender, message.content, message.timestamp.isoformat())
                )
    
    def load_chat(self, chat_id: str) -> Chat:
        """Carica una chat dal database"""
        with sqlite3.connect(self.db_path) as conn:
            # Carica info chat
            chat_row = conn.execute(
                'SELECT chat_id, participants FROM chats WHERE chat_id = ?',
                (chat_id,)
            ).fetchone()
            
            if not chat_row:
                raise ValueError(f"Chat {chat_id} non trovata")
            
            participants = json.loads(chat_row[1])
            chat = Chat(chat_row[0], participants)
            
            # Carica messaggi
            messages_rows = conn.execute(
                '''SELECT sender, content, timestamp 
                   FROM messages WHERE chat_id = ? 
                   ORDER BY timestamp''',
                (chat_id,)
            ).fetchall()
            
            for sender, content, timestamp in messages_rows:
                chat.add_message(Message(sender, content, datetime.fromisoformat(timestamp)))
            
            return chat
    
    def get_all_chats(self) -> List[Chat]:
        """Carica tutte le chat dal database"""
        with sqlite3.connect(self.db_path) as conn:
            chat_rows = conn.execute('SELECT chat_id FROM chats').fetchall()
            chats = []
            
            for (chat_id,) in chat_rows:
                try:
                    chats.append(self.load_chat(chat_id))
                except ValueError:
                    continue
            
            return chats
    
    def get_chat_list(self) -> List[str]:
        """Restituisce la lista degli ID chat"""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute('SELECT chat_id FROM chats ORDER BY created_at').fetchall()
            return [row[0] for row in rows]

# ==================== GESTIONE BACKUP ====================

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def export_json(self, chats: List[Chat], filename: str = None) -> str:
        """Esporta le chat in formato JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_backup_{timestamp}.json"
        
        filepath = os.path.join(self.backup_dir, filename)
        
        data = {
            'export_date': datetime.now().isoformat(),
            'version': '1.0',
            'chats': [chat.to_dict() for chat in chats]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def import_json(self, filepath: str) -> List[Chat]:
        """Importa chat da file JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Chat.from_dict(chat_data) for chat_data in data['chats']]
    
    def export_pickle(self, chats: List[Chat], filename: str = None) -> str:
        """Esporta le chat in formato pickle (più efficiente)"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_backup_{timestamp}.pkl"
        
        filepath = os.path.join(self.backup_dir, filename)
        
        with open(filepath, 'wb') as f:
            pickle.dump(chats, f)
        
        return filepath
    
    def import_pickle(self, filepath: str) -> List[Chat]:
        """Importa chat da file pickle"""
        with open(filepath, 'rb') as f:
            chats = pickle.load(f)
        return chats
    
    def export_txt(self, chats: List[Chat], filename: str = None) -> str:
        """Esporta le chat in formato testo leggibile"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_backup_{timestamp}.txt"
        
        filepath = os.path.join(self.backup_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"=== BACKUP CHAT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
            
            for chat in chats:
                f.write(f"Chat: {chat.chat_id}\n")
                f.write(f"Partecipanti: {', '.join(chat.participants)}\n")
                f.write("-" * 50 + "\n")
                
                for message in chat.messages:
                    f.write(f"[{message.timestamp.strftime('%Y-%m-%d %H:%M')}] ")
                    f.write(f"{message.sender}: {message.content}\n")
                
                f.write("\n" + "="*50 + "\n\n")
        
        return filepath
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """Lista tutti i backup disponibili"""
        backups = []
        for file in os.listdir(self.backup_dir):
            filepath = os.path.join(self.backup_dir, file)
            if os.path.isfile(filepath):
                stats = os.stat(filepath)
                backups.append({
                    'filename': file,
                    'path': filepath,
                    'size': stats.st_size,
                    'modified': datetime.fromtimestamp(stats.st_mtime)
                })
        
        return sorted(backups, key=lambda x: x['modified'], reverse=True)

# ==================== APPLICAZIONE PRINCIPALE ====================

class MessagingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Messaging App")
        self.root.geometry("800x600")
        
        # Inizializza componenti
        self.db = ChatDatabase()
        self.backup_mgr = BackupManager()
        self.current_user = "Utente1"
        self.current_chat = None
        
        # Crea interfaccia
        self.create_widgets()
        self.load_chats()
        
        # Auto-save ogni 30 secondi
        self.auto_save()
    
    def create_widgets(self):
        """Crea l'interfaccia grafica"""
        # Frame principale
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame sinistro (lista chat)
        left_frame = ttk.Frame(main_frame, width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Lista chat
        ttk.Label(left_frame, text="Chat", font=('Arial', 12, 'bold')).pack(pady=5)
        self.chat_listbox = tk.Listbox(left_frame)
        self.chat_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.chat_listbox.bind('<<ListboxSelect>>', self.on_chat_select)
        
        # Pulsanti gestione chat
        chat_buttons_frame = ttk.Frame(left_frame)
        chat_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(chat_buttons_frame, text="Nuova Chat", 
                  command=self.new_chat).pack(fill=tk.X, pady=2)
        ttk.Button(chat_buttons_frame, text="Elimina Chat", 
                  command=self.delete_chat).pack(fill=tk.X, pady=2)
        
        # Frame destro (messaggi)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Info chat corrente
        self.chat_info_label = ttk.Label(right_frame, text="Seleziona una chat", 
                                        font=('Arial', 10, 'bold'))
        self.chat_info_label.pack(pady=5)
        
        # Area messaggi
        messages_frame = ttk.Frame(right_frame)
        messages_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.messages_text = tk.Text(messages_frame, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(messages_frame, command=self.messages_text.yview)
        self.messages_text.configure(yscrollcommand=scrollbar.set)
        
        self.messages_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Input messaggio
        input_frame = ttk.Frame(right_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.message_entry = ttk.Entry(input_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', self.send_message)
        
        ttk.Button(input_frame, text="Invia", 
                  command=self.send_message).pack(side=tk.RIGHT)
        
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        backup_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Backup", menu=backup_menu)
        backup_menu.add_command(label="Esporta JSON", command=self.export_json)
        backup_menu.add_command(label="Esporta Pickle", command=self.export_pickle)
        backup_menu.add_command(label="Esporta TXT", command=self.export_txt)
        backup_menu.add_separator()
        backup_menu.add_command(label="Importa JSON", command=self.import_json)
        backup_menu.add_command(label="Importa Pickle", command=self.import_pickle)
        backup_menu.add_command(label="Lista Backup", command=self.show_backups)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_chats(self):
        """Carica la lista delle chat"""
        self.chat_listbox.delete(0, tk.END)
        chats = self.db.get_chat_list()
        for chat_id in chats:
            self.chat_listbox.insert(tk.END, chat_id)
    
    def on_chat_select(self, event):
        """Gestisce la selezione di una chat"""
        selection = self.chat_listbox.curselection()
        if selection:
            chat_id = self.chat_listbox.get(selection[0])
            try:
                self.current_chat = self.db.load_chat(chat_id)
                self.display_messages()
                self.chat_info_label.config(
                    text=f"Chat: {chat_id} - Partecipanti: {', '.join(self.current_chat.participants)}"
                )
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile caricare la chat: {e}")
    
    def display_messages(self):
        """Mostra i messaggi della chat corrente"""
        self.messages_text.config(state=tk.NORMAL)
        self.messages_text.delete(1.0, tk.END)
        
        if self.current_chat:
            for message in self.current_chat.messages:
                self.messages_text.insert(tk.END, f"{message}\n")
        
        self.messages_text.config(state=tk.DISABLED)
        self.messages_text.see(tk.END)
    
    def send_message(self, event=None):
        """Invia un messaggio"""
        if not self.current_chat:
            messagebox.showwarning("Attenzione", "Seleziona una chat prima di inviare messaggi")
            return
        
        content = self.message_entry.get().strip()
        if not content:
            return
        
        message = Message(self.current_user, content)
        self.current_chat.add_message(message)
        
        self.display_messages()
        self.message_entry.delete(0, tk.END)
        self.save_current_chat()
    
    def save_current_chat(self):
        """Salva la chat corrente"""
        if self.current_chat:
            self.db.save_chat(self.current_chat)
            self.status_var.set(f"Chat salvata: {datetime.now().strftime('%H:%M:%S')}")
    
    def new_chat(self):
        """Crea una nuova chat"""
        dialog = NewChatDialog(self.root)
        if dialog.result:
            chat_id, participants = dialog.result
            new_chat = Chat(chat_id, participants)
            self.db.save_chat(new_chat)
            self.load_chats()
            self.status_var.set(f"Nuova chat creata: {chat_id}")
    
    def delete_chat(self):
        """Elimina la chat selezionata"""
        selection = self.chat_listbox.curselection()
        if not selection:
            return
        
        chat_id = self.chat_listbox.get(selection[0])
        if messagebox.askyesno("Conferma", f"Eliminare la chat '{chat_id}'?"):
            with sqlite3.connect(self.db.db_path) as conn:
                conn.execute('DELETE FROM chats WHERE chat_id = ?', (chat_id,))
                conn.execute('DELETE FROM messages WHERE chat_id = ?', (chat_id,))
            
            self.load_chats()
            self.current_chat = None
            self.display_messages()
            self.chat_info_label.config(text="Seleziona una chat")
            self.status_var.set(f"Chat eliminata: {chat_id}")
    
    def export_json(self):
        """Esporta tutte le chat in JSON"""
        chats = self.db.get_all_chats()
        if not chats:
            messagebox.showwarning("Attenzione", "Nessuna chat da esportare")
            return
        
        filepath = self.backup_mgr.export_json(chats)
        messagebox.showinfo("Successo", f"Backup JSON creato:\n{filepath}")
    
    def export_pickle(self):
        """Esporta tutte le chat in Pickle"""
        chats = self.db.get_all_chats()
        if not chats:
            messagebox.showwarning("Attenzione", "Nessuna chat da esportare")
            return
        
        filepath = self.backup_mgr.export_pickle(chats)
        messagebox.showinfo("Successo", f"Backup Pickle creato:\n{filepath}")
    
    def export_txt(self):
        """Esporta tutte le chat in TXT"""
        chats = self.db.get_all_chats()
        if not chats:
            messagebox.showwarning("Attenzione", "Nessuna chat da esportare")
            return
        
        filepath = self.backup_mgr.export_txt(chats)
        messagebox.showinfo("Successo", f"Backup TXT creato:\n{filepath}")
    
    def import_json(self):
        """Importa chat da file JSON"""
        filepath = filedialog.askopenfilename(
            title="Seleziona file JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            try:
                chats = self.backup_mgr.import_json(filepath)
                for chat in chats:
                    self.db.save_chat(chat)
                self.load_chats()
                messagebox.showinfo("Successo", f"Importate {len(chats)} chat da JSON")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile importare: {e}")
    
    def import_pickle(self):
        """Importa chat da file Pickle"""
        filepath = filedialog.askopenfilename(
            title="Seleziona file Pickle",
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
        )
        if filepath:
            try:
                chats = self.backup_mgr.import_pickle(filepath)
                for chat in chats:
                    self.db.save_chat(chat)
                self.load_chats()
                messagebox.showinfo("Successo", f"Importate {len(chats)} chat da Pickle")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile importare: {e}")
    
    def show_backups(self):
        """Mostra la lista dei backup disponibili"""
        backups = self.backup_mgr.list_backups()
        BackupListDialog(self.root, backups)
    
    def auto_save(self):
        """Salvataggio automatico periodico"""
        if self.current_chat:
            self.save_current_chat()
        self.root.after(30000, self.auto_save)  # Ogni 30 secondi

# ==================== DIALOGHI ====================

class NewChatDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuova Chat")
        self.dialog.geometry("300x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        ttk.Label(self.dialog, text="ID Chat:").pack(pady=5)
        self.id_entry = ttk.Entry(self.dialog, width=30)
        self.id_entry.pack(pady=5)
        
        ttk.Label(self.dialog, text="Partecipanti (separati da virgola):").pack(pady=5)
        self.part_entry = ttk.Entry(self.dialog, width=30)
        self.part_entry.pack(pady=5)
        self.part_entry.insert(0, "Utente1, Utente2")
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Crea", 
                  command=self.create).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annulla", 
                  command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.dialog.wait_window()
    
    def create(self):
        chat_id = self.id_entry.get().strip()
        participants = [p.strip() for p in self.part_entry.get().split(',')]
        
        if not chat_id or not participants:
            messagebox.showwarning("Attenzione", "Inserisci ID chat e partecipanti")
            return
        
        self.result = (chat_id, participants)
        self.dialog.destroy()

class BackupListDialog:
    def __init__(self, parent, backups):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Lista Backup")
        self.dialog.geometry("500x300")
        
        tree = ttk.Treeview(self.dialog, columns=('Size', 'Modified'), show='headings')
        tree.heading('#0', text='Filename')
        tree.heading('Size', text='Dimensione')
        tree.heading('Modified', text='Modificato')
        
        for backup in backups:
            tree.insert('', 'end', text=backup['filename'],
                       values=(f"{backup['size']} bytes", 
                              backup['modified'].strftime('%Y-%m-%d %H:%M')))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(self.dialog, text="Chiudi", 
                  command=self.dialog.destroy).pack(pady=10)

# ==================== AVVIO APPLICAZIONE ====================

def main():
    root = tk.Tk()
    app = MessagingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()