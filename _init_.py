from flask import Flask, jsonify, request, Blueprint
# from flask_cors import CORS
import sqlite3
import os

def database_exists(db_file):
    return os.path.isfile(db_file)

def create_app(config_file="config.py"):
    app = Flask(__name__)
    # cors = CORS(app)
    app.config.from_pyfile(config_file)

    db_file = 'CRM.db'

    if not database_exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS KhachHangTiemNang;")
        cursor.execute("DROP TABLE IF EXISTS NhaCungCap;")

        cursor.execute('''CREATE TABLE KhachHangTiemNang (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ten CHAR(255) NOT NULL,
            Gmail CHAR(255) UNIQUE NOT NULL,
            SDT CHAR(20) NOT NULL,
            NgheNghiep CHAR(255),
            ThongTinChung TEXT,
            NhaCungCapID INTEGER,
            FOREIGN KEY (NhaCungCapID) REFERENCES NhaCungCap (ID)
        );''')

        cursor.execute('''CREATE TABLE NhaCungCap (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ten CHAR(255) NOT NULL,
            DiaChi CHAR(255),
            CC CHAR(255),
            BCC CHAR(255),
            ThongTinChung TEXT,
            KhachHangTiemNangID INTEGER,
            FOREIGN KEY (KhachHangTiemNangID) REFERENCES KhachHangTiemNang (ID)
        );''')

        cursor.execute("INSERT INTO KhachHangTiemNang (Ten, Gmail, SDT, NgheNghiep, ThongTinChung) VALUES (?, ?, ?, ?, ?);",
                   ('Tên Khách Hàng', 'email@example.com', 'Số Điện Thoại', 'Nghề Nghiệp', 'Thông Tin Chung'))

        cursor.execute("INSERT INTO KhachHangTiemNang (Ten, Gmail, SDT, NgheNghiep, ThongTinChung) VALUES (?, ?, ?, ?, ?);",
                    ('Nguyễn Văn A', 'nguyenvana@example.com', '123456789', 'Kỹ sư', 'Thông tin chi tiết về khách hàng'))

        cursor.execute("INSERT INTO NhaCungCap (Ten, DiaChi, CC, BCC, ThongTinChung) VALUES (?, ?, ?, ?, ?);",
                    ('Tên Nhà Cung Cấp', 'Địa chỉ nhà cung cấp', 'CC Email', 'BCC Email', 'Thông Tin Chung'))

        cursor.execute("INSERT INTO NhaCungCap (Ten, DiaChi, CC, BCC, ThongTinChung) VALUES (?, ?, ?, ?, ?);",
                    ('Công ty ABC', '123 Đường ABC, Thành phố XYZ', 'cc@example.com', 'bcc@example.com', 'Thông tin chi tiết về nhà cung cấp'))

        conn.commit()
        conn.close()

    # API route to show information
    @app.route('/khachhangtiemnang/<int:id>', methods=['GET'])
    def get_khach_hang_tiem_nang(id):
        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM KhachHangTiemNang WHERE ID=?", (id,))
        khach_hang = cursor.fetchone()
        conn.close()

        if khach_hang is not None:
            return jsonify({
                'ID': khach_hang[0],
                'Ten': khach_hang[1],
                'Gmail': khach_hang[2],
                'SDT': khach_hang[3],
                'NgheNghiep': khach_hang[4],
                'ThongTinChung': khach_hang[5]
            })
        else:
            return jsonify({'error': 'KhachHangTiemNang not found'}), 404

    # API route to show all information
    @app.route('/khachhangtiemnang', methods=['GET'])
    def get_all_khach_hang_tiem_nang():
        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM KhachHangTiemNang")
        khach_hang_list = cursor.fetchall()
        conn.close()

        khach_hang_data = []
        for khach_hang in khach_hang_list:
            khach_hang_data.append({
                'ID': khach_hang[0],
                'Ten': khach_hang[1],
                'Gmail': khach_hang[2],
                'SDT': khach_hang[3],
                'NgheNghiep': khach_hang[4],
                'ThongTinChung': khach_hang[5]
            })

        return jsonify(khach_hang_data)
    # API route to add new customer
    @app.route('/khachhangtiemnang', methods=['POST'])
    def add_khach_hang_tiem_nang():
        data = request.get_json()
        ten = data.get('Ten')
        gmail = data.get('Gmail')
        sdt = data.get('SDT')
        nghenghiep = data.get('NgheNghiep')
        thongtinchung = data.get('ThongTinChung')

        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO KhachHangTiemNang (Ten, Gmail, SDT, NgheNghiep, ThongTinChung) VALUES (?, ?, ?, ?, ?)",
                    (ten, gmail, sdt, nghenghiep, thongtinchung))
        conn.commit()
        conn.close()

        return jsonify({'message': 'KhachHangTiemNang added successfully'}), 201

    # API route to update customer information
    @app.route('/khachhangtiemnang/<int:id>', methods=['PUT'])
    def update_khach_hang_tiem_nang(id):
        data = request.get_json()
        ten = data.get('Ten')
        gmail = data.get('Gmail')
        sdt = data.get('SDT')
        nghenghiep = data.get('NgheNghiep')
        thongtinchung = data.get('ThongTinChung')

        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE KhachHangTiemNang SET Ten=?, Gmail=?, SDT=?, NgheNghiep=?, ThongTinChung=? WHERE ID=?",
                    (ten, gmail, sdt, nghenghiep, thongtinchung, id))
        conn.commit()
        conn.close()

        return jsonify({'message': 'KhachHangTiemNang updated successfully'})

    # API route to delete customer
    @app.route('/khachhangtiemnang/<int:id>', methods=['DELETE'])
    def delete_khach_hang_tiem_nang(id):
        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM KhachHangTiemNang WHERE ID=?", (id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'KhachHangTiemNang deleted successfully'})
    
# Nha Cung Cap
    # API route to get information of a specific NhaCungCap by ID
    @app.route('/nhacungcap/<int:id>', methods=['GET'])
    def get_nha_cung_cap_by_id(id):
        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NhaCungCap WHERE ID=?", (id,))
        nha_cung_cap = cursor.fetchone()
        conn.close()

        if nha_cung_cap is not None:
            return jsonify({
                'ID': nha_cung_cap[0],
                'Ten': nha_cung_cap[1],
                'DiaChi': nha_cung_cap[2],
                'CC': nha_cung_cap[3],
                'BCC': nha_cung_cap[4],
                'ThongTinChung': nha_cung_cap[5]
            })
        else:
            return jsonify({'error': 'NhaCungCap not found'}), 404
        
    # Get all nhacungcap
    @app.route('/nhacungcap', methods=['GET'])
    def get_all_nha_cung_cap():
        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NhaCungCap")
        nha_cung_cap_list = cursor.fetchall()
        conn.close()

        nha_cung_cap_data = []
        for nha_cung_cap in nha_cung_cap_list:
            nha_cung_cap_data.append({
                'ID': nha_cung_cap[0],
                'Ten': nha_cung_cap[1],
                'DiaChi': nha_cung_cap[2],
                'CC': nha_cung_cap[3],
                'BCC': nha_cung_cap[4],
                'ThongTinChung': nha_cung_cap[5]
            })

        return jsonify(nha_cung_cap_data)

    # API route to add new supplier
    @app.route('/nhacungcap', methods=['POST'])
    def add_nha_cung_cap():
        data = request.get_json()
        ten = data.get('Ten')
        dia_chi = data.get('DiaChi')
        cc = data.get('CC')
        bcc = data.get('BCC')
        thong_tin_chung = data.get('ThongTinChung')

        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NhaCungCap (Ten, DiaChi, CC, BCC, ThongTinChung) VALUES (?, ?, ?, ?, ?)",
                    (ten, dia_chi, cc, bcc, thong_tin_chung))
        conn.commit()
        conn.close()

        return jsonify({'message': 'NhaCungCap added successfully'}), 201

    # API route to update supplier information
    @app.route('/nhacungcap/<int:id>', methods=['PUT'])
    def update_nha_cung_cap(id):
        data = request.get_json()
        ten = data.get('Ten')
        dia_chi = data.get('DiaChi')
        cc = data.get('CC')
        bcc = data.get('BCC')
        thong_tin_chung = data.get('ThongTinChung')

        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE NhaCungCap SET Ten=?, DiaChi=?, CC=?, BCC=?, ThongTinChung=? WHERE ID=?",
                    (ten, dia_chi, cc, bcc, thong_tin_chung, id))
        conn.commit()
        conn.close()

        return jsonify({'message': 'NhaCungCap updated successfully'})

    # API route to delete supplier
    @app.route('/nhacungcap/<int:id>', methods=['DELETE'])
    def delete_nha_cung_cap(id):
        conn = sqlite3.connect('CRM.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NhaCungCap WHERE ID=?", (id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'NhaCungCap deleted successfully'})
        
    return app
