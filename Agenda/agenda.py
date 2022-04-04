from PyQt5 import uic, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem
from reportlab.pdfgen import canvas
from functools import partial

banco = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="",
    database="agenda"
)


def tela_agenda():
    listar_contatos.close()
    agenda.show()

    # Dando funcionalidade aos botões na tela agenda
    agenda.btn_cadastrar.clicked.connect(cadastrar_contato)
    agenda.btn_consultar.clicked.connect(consultar_contatos)


def cadastrar_contato():
    campo_nome = agenda.nome.text()
    campo_email = agenda.email.text()
    campo_telefone = agenda.telefone.text()

    if agenda.telefone_residencial.isChecked():
        tipo_telefone = "Residencial"
    elif agenda.celular.isChecked():
        tipo_telefone = "Celular"
    else:
        tipo_telefone = "Não informado"

    cursor = banco.cursor()
    comando_sql = "INSERT INTO contatos (nome, email, telefone, tipoTelefone) VALUES (%s, %s, %s, %s)"
    dados = (str(campo_nome), str(campo_email), str(campo_telefone), tipo_telefone)
    cursor.execute(comando_sql, dados)
    banco.commit()
    agenda.close()
    print("Contato cadastrado com sucesso!")


def consultar_contatos():
    listar_contatos.show()
    agenda.close()
    alterar_contatos.close()

    cursor = banco.cursor()
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    contatos_lidos = cursor.fetchall()

    listar_contatos.tabelaContatos.setRowCount(len(contatos_lidos))
    listar_contatos.tabelaContatos.setColumnCount(5)

    for i in range(0, len(contatos_lidos)):
        for f in range(0, 5):
            listar_contatos.tabelaContatos.setItem(i, f, QTableWidgetItem(str(contatos_lidos[i][f])))

    # Dando funcionalidade aos botões na tela listaContatos
    listar_contatos.btn_voltar.clicked.connect(tela_agenda)
    listar_contatos.btn_gerar_pdf.clicked.connect(gerar_pdf)
    listar_contatos.btn_alterar_contato.clicked.connect(alterar_contato)
    listar_contatos.btn_excluir_contato.clicked.connect(excluir_contato)


def excluir_contato():
    linha_contato = listar_contatos.tabelaContatos.currentRow()
    listar_contatos.tabelaContatos.removeRow(linha_contato)
    cursor = banco.cursor()
    comando_sql = "SELECT id FROM contatos"
    cursor.execute(comando_sql)
    contatos_lidos = cursor.fetchall()
    valor_id = contatos_lidos[linha_contato][0]
    cursor.execute(f"DELETE FROM contatos WHERE id={str(valor_id)}")
    banco.commit()
    print("Contato excluido com sucesso!")


def gerar_pdf():
    cursor = banco.cursor()
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    contatos_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("lista_contatos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Lista de Contatos")

    pdf.setFont("Times-Bold", 18)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "NOME")
    pdf.drawString(210, 750, "EMAIL")
    pdf.drawString(410, 750, "TELEFONE")
    pdf.drawString(510, 750, "TIPO DE CONTATO")

    for i in range(0, len(contatos_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(contatos_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(contatos_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(contatos_lidos[i][2]))
        pdf.drawString(410, 750 - y, str(contatos_lidos[i][3]))
        pdf.drawString(510, 750 - y, str(contatos_lidos[i][4]))

    pdf.save()
    print("PDF gerado com sucesso!")


def alterar_contato():
    global id

    linha_contato = listar_contatos.tabelaContatos.currentRow()
    cursor = banco.cursor()
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    contatos_lidos = cursor.fetchall()

    valor_id = contatos_lidos[linha_contato][0]
    id = valor_id
    nome = contatos_lidos[linha_contato][1]
    email = contatos_lidos[linha_contato][2]
    telefone = contatos_lidos[linha_contato][3]
    tipotelefone = contatos_lidos[linha_contato][4]

    listar_contatos.close()
    alterar_contatos.show()

    alterar_contatos.campo_nome.setText(nome)
    alterar_contatos.campo_email.setText(email)
    alterar_contatos.campo_telefone.setText(telefone)

    alterar_contatos.btn_consultar.clicked.connect(consultar_contatos)
    alterar_contatos.btn_alterar.clicked.connect(salvar_contato)


def salvar_contato():
    global id

    nome = alterar_contatos.campo_nome.text()
    email = alterar_contatos.campo_email.text()
    telefone = alterar_contatos.campo_telefone.text()

    cursor = banco.cursor()
    cursor.execute(f"update contatos set email='{nome}', email='{email}', "
                   f"telefone='{telefone}' where id={id}")
    banco.commit()
    print("Contato alterado com sucesso!")


app = QtWidgets.QApplication([])
agenda = uic.loadUi("agenda.ui")
listar_contatos = uic.loadUi("listaContatos.ui")
alterar_contatos = uic.loadUi("alterarContatos.ui")

tela_agenda()
app.exec()


