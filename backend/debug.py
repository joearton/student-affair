import sqlite3
import pydot

# Koneksi ke database SQLite
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Dapatkan semua tabel
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

graph = pydot.Dot(graph_type="digraph")

# Tambahkan node untuk setiap tabel dengan info kolom
for table in tables:
    # Dapatkan informasi kolom
    cursor.execute(f"PRAGMA table_info({table});")
    columns = cursor.fetchall()  # Hasilnya adalah (cid, name, type, notnull, dflt_value, pk)
    
    # Buat label tabel dengan informasi kolom
    label = f"<<table border='1' cellborder='0' cellspacing='0'>"
    label += f"<tr><td bgcolor='lightblue'><b>{table}</b></td></tr>"
    
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        pk = "PK" if col[5] else ""  # Primary Key jika ada
        label += f"<tr><td align='left'>{col_name} ({col_type}) {pk}</td></tr>"
    
    label += "</table>>"
    
    # Tambahkan node dengan label ke graph
    graph.add_node(pydot.Node(table, shape="none", label=label))

# Tambahkan relasi antar tabel
for table in tables:
    cursor.execute(f"PRAGMA foreign_key_list({table});")
    for fk in cursor.fetchall():
        from_table = table
        from_column = fk[3]  # Kolom sumber
        to_table = fk[2]  # Nama tabel yang dirujuk
        to_column = fk[4]  # Kolom tujuan
        
        # Tambahkan edge dengan label kolom
        graph.add_edge(pydot.Edge(
            from_table, to_table, 
            label=f"{from_column} → {to_column}", 
            fontsize="10"
        ))

# Simpan diagram sebagai gambar
graph.write_png("diagram_relasi_dengan_kolom.png")
print("Diagram relasi dengan kolom disimpan sebagai 'diagram_relasi_dengan_kolom.png'")
