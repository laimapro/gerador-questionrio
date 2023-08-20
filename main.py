from io import StringIO
import streamlit as st
import pandas as pd
import random
import xlsxwriter
import openpyxl
from PIL import Image
import os
import numpy as np
import itertools

def main():
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    st.write("Bem-vindo ao LGQIA+! 🕰️ Agora são " + current_time)

if __name__ == '__main__':
    main()

st.markdown(f"<br>", unsafe_allow_html = True)


col1, col2 = st.columns(2)
with col1:
    image = Image.open('img/laima-logo.png')
    st.image(image, caption=None, width=150)
with col2:
    image = Image.open('img/universidade.png')
    st.image(image, caption=None, width=150)

with open("css/quest_sort.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


def matrix(auxFinal, questions, subFolderInfo):
    i=0
    j = 0
    matrix = []
    #CRIA LISTA QUE GUARDA O NÚMERO DE VEZES Q CADA ITEM APARECE NOS QUESTIONÁRIOS
    for i in range(len(questions)):
        matrix.append(0)
    i = 0
    while i < len(auxFinal):
        j = 0
        while j < len(questions):
            if questions[j] in auxFinal[i]:
                matrix[j]=matrix[j] + 1
                j = j + 1
            else:
                j = j + 1
        i = i + 1
    data = pd.DataFrame({'Itens na base de dados':questions, 'Número de vezes que cada item será apresentado para avaliação':matrix})
    data.to_excel(os.path.join(subFolderInfo, "Registro.xlsx"), index=False)


def sampleCalculator(sampl, numQuestion, a, b):
    dataLen = a+b
    if (numQuestion-b)!=0:
        subjectQuan = (a*(numQuestion-b)*sampl)/(numQuestion-b)
    else:
        subjectQuan = sampl * numQuestion
    return subjectQuan

def sampleCalculator_one(sampl, numQuestion, a):
    dataLen = a
    subjectQuan = (dataLen*numQuestion*sampl)/numQuestion
    return subjectQuan

#FUNÇÃO QUE GERA O ARQUIVO PARA DOWNLOAD
def generateDownload(auxFinal, subFolderQuest):
    i= 0
    my_bar = st.progress(50)
    while i < len(auxFinal):
        col1 = f"Questionário {i+1}"
        data = pd.DataFrame({col1:auxFinal[i]})
        data.to_excel(os.path.join(subFolderQuest, f"questionário_{i+1}.xlsx"), index=False)
        i = i + 1
    my_bar.progress(100)
    st.success("Questionários baixados")

#FUNÇÃO QUE REMOVE OU NÃO QUESTIONÁRIOS
def removeQuest (auxFinal, subjectQuan, questions, subFolderQuest, subFolderInfo):
    i = 0
    if len(auxFinal)==subjectQuan:
        matrix(auxFinal, questions, subFolderInfo)
        generateDownload(auxFinal, subFolderQuest)
    elif len(auxFinal) != subjectQuan:
        i = 0
        while len(auxFinal) != subjectQuan:
            auxFinal.remove(auxFinal[i])
            i = i + 1
        matrix(auxFinal, questions, subFolderInfo)
        generateDownload(auxFinal, subFolderQuest)

#FUNÇÃO PARA UPLOAD DO ARQUIVO DA BASE COMPLEMENTAR
def file_type_g(uploaded_file_g):
    a = []
    file_t = "xlsx"
    for uploaded_file in uploaded_file_g:
        bytes_data = uploaded_file.read()
        if file_t=="xlsx":
            xlsx = openpyxl.load_workbook(uploaded_file, read_only=True)
            ## getting the sheet to active
            sheet = xlsx.active
            ## getting the reference of the cells which we want to get the data from
            rows = sheet.rows 
            for row in sheet.iter_rows(min_row=1, max_col=1):
                for cell in row:
                    a.append(cell.value)
            st.write("O tamanho da sua base é:", len(a))
            st.write(a)
    return a


st.sidebar.title("Menu")
paginaSelecionada = st.sidebar.radio("", ('LGQIA+ Página Principal','LGQIA+ Gerar Questionários Inteligentes', 'LGQIA+ Informações Gerais'),index=0)


#LGQIA+ PÁGINA PRINCIPAL
if paginaSelecionada == 'LGQIA+ Página Principal' :

    col3, col4 = st.columns(2)
    with col3:
        st.write("Aprenda como usar o Laima - gerador de questionários Inteligente com Análise Automatizada (LGQIA+), assistindo ao tutorial à esquerda")
    with col4:
        st.video("video/azul.mp4")

#ADICIONAR AUDIO
    st.markdown('<center>Ouça o nome do "Laboratory of Artificial Intelligence and Machine Aid"</center>', unsafe_allow_html=True)

    st.audio("audio/LAIMA.mp3", format='audio/mp3')

    st.title("Laima - gerador de questionários Inteligente com Análise Automatizada (LGQIA+)")
    st.write("O Laima - LGQIA+ gera questionários a partir da base de dados que você fornecer. O Laima - LGQIA pode embaralhar as perguntas ou itens de seu questionário para você e apresentá-lo aleatoriamente a quantos respondentes, avaliadores ou observadores você determinar. Com o Laima - gerador de questionários Inteligente com Análise Automatizada (LGQIA+) você pode imprimir seus questionários ou disponibilizá-los na rede para que possam ser respondidos, conforme a necessidade de sua pesquisa. O Laima - gerador de questionários Inteligente comAnálise Automatizada (LGQIA+) vai, ainda, ajudar você analisar as respostas dos sujeitos de sua pesquisa e apresentar os dados encontrados em tabelas e gráficos elegantes, profissionais e fáceis de serem entendidos. Experimente o O Laima - gerador de questionários Inteligente com Análise Automatizada (LGQIA+) e veja o que mais você poderá fazer. Usar o O Laima - gerador de questionários Inteligente com Análise Automatizada (LGQIA+) é fácil de aprender, rápido e intuitivo.")

#PÁGINA PARA GERAR QUESTIONÁRIOS
elif paginaSelecionada == 'LGQIA+ Gerar Questionários Inteligentes':
    
#FORMULÁRIO 1
    st.title("Gerar Questionários Inteligentes")
    with st.form(key="form0"):
        uploaded_file_g = "none" ; uploaded_file_o = "none" ; uploaded_file_c = "none"
        uploaded_file_g = st.file_uploader("Se você possui uma base de dados geral única faça o upload do arquivo xlsx aqui.", accept_multiple_files=True)
        uploaded_file_o = st.file_uploader("Se você possui uma base de dados obrigatória faça o upload do arquivo xlsx aqui.", accept_multiple_files=True)
        uploaded_file_c = st.file_uploader("Se você possui uma base de dados complementar faça o upload do arquivo xlsx aqui.", accept_multiple_files=True)
        btn0 = st.form_submit_button(label="Submeter")
        #MENSAGEM DE SUCESSO
        if (btn0):
            st.success("Submetido!")       
    a = "none"
    b = "none"
    if (btn0):
        if (uploaded_file_g != "none"):
            a = file_type_g(uploaded_file_g)
        if (uploaded_file_o != "none") and (uploaded_file_c != "none"):
            b = file_type_g(uploaded_file_o)
            a = file_type_g(uploaded_file_c)

   #RADIO BUTTONS
    form01 = st.form(key="form01")
    alea = 0
    if (a != "none") and (b != "none"):
        alea = 2
        firstLast_radio = form01.radio("", ("Desejo que os  itens comuns apareçam no início dos questionários", "Desejo que os itens comuns apareçam no final de cada questionário", "Desejo que as itens comuns apareçam embaralhadas entre os itens aleatótios"), index=0)
        if firstLast_radio == "Desejo que os  itens comuns apareçam no início dos questionários":
            firstLast=0
        elif firstLast_radio == "Desejo que os itens comuns apareçam no final de cada questionário":
            firstLast=1
        else:
            firstLast=2
        mix_radio = form01.radio("",("Desejo que os itens comuns apareçam na mesma ordem para todos os respondentes", "Desejo que os itens comuns apareçam em diferentes ordens para os respondentes"), index=0)
        if mix_radio == "Desejo que os itens comuns apareçam mesma ordem para todos os respondentes.":
            mix = 0
        else:
            mix = 1
    elif ((a != "none") and (b == "none")) or ((a == "none") and (b == "none")):
        radio_button = form01.radio("",("Esta opção gera questionários na ordem em que estão na base de dados", "Esta opção gera questionários, embaralhando os itens, a partir de como estão na base de dados", "Esta opção gera diferentes questionários, embaralhando os itens, a partir de como estão na base de dados"),index=0)
        if radio_button == "Esta opção gera questionários na ordem em que estão na base de dados":
            alea = 0
        elif radio_button == "Esta opção gera questionários, embaralhando os itens, a partir de como estão na base de dados":
            alea = 3
        elif radio_button == "Esta opção gera diferentes questionários, embaralhando os itens, a partir de como estão na base de dados":
            alea = 1
    
    btn1 = form01.form_submit_button(label="Submeter")
    #MENSAGEM DE SUCESSO
    if (btn1):
        st.success("Submetido!")    

    form2 = st.form(key="form2")
    numQuestion=0
    sampl = 0
    if ((alea == 2) or (alea == 1)):
        numQuestion = form2.number_input("Quantos ítens você quer em cada questionário gerado?", min_value=0, value=0)
        sampl = form2.number_input("Quantas vezes cada ítem deverá ser respondido?",min_value=0, value=0)
    else:
        sampl = form2.number_input("Quantas vezes cada ítem deverá ser respondido?",min_value=0, value=0)
    btn2 = form2.form_submit_button(label="Submeter")
    #MENSAGEM DE SUCESSO
    if (btn2):
        st.success("Submetido!")
   
    #FORMULÁRIO 7
    form7 = st.form(key="form7")   
    subjectQuan=0
    if (sampl !=0) and alea == 2:
        subjectQuan = sampleCalculator(sampl, numQuestion, len(a), len(b))
    elif (sampl !=0) and alea==1:
        subjectQuan = sampleCalculator_one(sampl, numQuestion, len(a))
    elif (sampl != 0) and ((alea == 0) or (alea == 3)):
        st.write(a)
        subjectQuan= len(a)*sampl

    #VERIFICA SE O USUÁRIO QUER USAR TODOS OS QUESTIONÁRIOS OU NÃO
    form7.write("Será gerada a seguinte quantidade de questionários:")
    form7.write(subjectQuan)
    newSubjectQuan=0
    newSubjectQuan=form7.number_input("Caso esteja pronta(o) para gerar os questionários conforme definido nos campos anteriores, clique no botão Submeter e Gerar Questionários seguinte. Se você deseja redefinir a quantidade de questionários a ser gerados agora, insira a nova quantidade desejada abaixo. Atenção! Essa alteração pode produzir questionários em que os itens não apareçam em mesma quantidade para avaliação.", min_value=0)
    if newSubjectQuan !=0:
        subjectQuan = newSubjectQuan
    btn7 = form7.form_submit_button("Submeter e gerar questionários.") 
    if (btn7):
        form7.warning("Seus questionários serão salvos no diretório Questionários Gerados, em sua pasta de downloads.")
        form7.success("Submetido!")
    



    #GERA NOVO DIRETÓRIO
    if (btn7):
        download_folder = os.path.expanduser("~/Downloads")
        directory = os.path.join(download_folder, "Arquivo_LGQIA+")

        if os.path.exists(directory):
            subdirectories = [
                os.path.join(directory, "Questionários_gerados"), 
                os.path.join(directory, "Registro")
                ]
            if (os.path.exists(subdirectories[0])) and (os.path.exists(subdirectories[1])):    
                subFolderQuest=subdirectories[0]
                subFolderInfo=subdirectories[1]

        if not os.path.exists(directory):
            os.makedirs(directory)
            subdirectories = [
                os.path.join(directory, "Questionários_gerados"), 
                os.path.join(directory, "Registro")
                ]
            if (not os.path.exists(subdirectories[0])) and (not os.path.exists(subdirectories[1])):
                os.makedirs(subdirectories[0])
                os.makedirs(subdirectories[1])
            subFolderQuest=subdirectories[0]
            subFolderInfo=subdirectories[1]
    
    st.write("subjectQuan é:",subjectQuan)
    st.write(a)
    if (alea == 0) and (btn7):
        questions = []
        if a is not None:
            questions = a
        i= 0
        j= 0
        auxFinal = []
        #GERA O QUESTIONÁRIO
        while (i < subjectQuan):
            j = 0
            aux = []
            while (j < len(questions)) and (i < subjectQuan):
                aux.append(questions[j])
                j =  j + 1
            st.write(aux)
            auxFinal.append(aux)
            i = i + 1  
        #DOWNLOAD DO ARQUIVO
        removeQuest(auxFinal, subjectQuan, questions, subFolderQuest, subFolderInfo)
    elif (alea == 3) and (btn7):
        questions = []
        if a is not None:
            questions = a
        i= 0
        j= 0
        auxFinal = []
        #GERA O QUESTIONÁRIO
        while (i < subjectQuan):
            j = 0
            aux = []
            random_questions = random.sample(questions, len(questions))
            while (j < len(questions)) and (i < subjectQuan):
                aux.append(questions[j])
                j =  j + 1
            auxFinal.append(aux)
            i = i + 1  
        #DOWNLOAD DO ARQUIVO
        removeQuest(auxFinal, subjectQuan, questions, subFolderQuest, subFolderInfo)

    elif (alea == 1) and (btn7):
        questions = []

        if a is not None:
            questions = a 

        #CRIA NOVO BANCO DE DADOS COM O TOTAL DE ÍTENS NECESSÁRIOS PARA ATENDER OS REQUISITOS
        i = 0
        j = 0
        baseLen = len(a)
        auxBase = []
        #GERA NOVA BASE DE DADOS DE MODO A ATENDER OS REQUISITOS SOLICITADOS
        random_questions = random.sample(questions, len(questions))
        while i < (subjectQuan*numQuestion):
            random_questions = random.sample(questions, len(questions))
            j = 0
            while j < len(random_questions):
                auxBase.append(random_questions[j])
                j =  j + 1
                i = i + 1

        i = 0
        j = 0
        t = 0
        aux = []
        auxBaseLen=len(auxBase)
        auxFinal=[]
        while (i < auxBaseLen):
            j = 0
            while (j < numQuestion) and (i < auxBaseLen):
                t = 0
                #VERIFICA SE O ÍTEM ESTÁ CONTIDO NA LISTA
                while auxBase[t] in aux:
                    t = t + 1
                aux.append(auxBase[t])
                auxBase.remove(auxBase[t])
                i = i + 1
                j = j + 1                    
            auxFinal.append(aux)
            aux = []
        #REMOVE OU NÃO QUESTIONÁRIOS
        removeQuest(auxFinal, subjectQuan, questions, subFolderQuest, subFolderInfo)


    elif (alea==2) and (btn7):
        questions = []
        fixed_questions = []

        if (a and b) is not None:
           questions=a
           fixed_questions=b
        new_questions = list(itertools.chain(fixed_questions, questions))
        i = 0
        j = 0
        auxBase=[]
        #DEFINE NOVA BASE DE DADOS
        random_questions = random.sample(questions, len(questions))
        while i < (subjectQuan*(numQuestion-len(b))):
            random_questions = random.sample(questions, len(questions))
            j = 0
            while j < len(random_questions):
                auxBase.append(random_questions[j])
                j =  j + 1
                i = i + 1              
        outputfile = []
        formsName = "Questionário"
        
        auxBaseLen=len(auxBase)
        auxFinal=[]
        if firstLast == 0:
            if mix == 0:
                j = 0
                i = 0
                t = 0
                while i < (auxBaseLen):
                    j = 0
                    aux = []
                    while (j < len(fixed_questions)) and (i < (auxBaseLen)):
                        aux.append(fixed_questions[j])
                        j = j + 1
                    j = 0  
                    while (j < (numQuestion - len(fixed_questions))) and (i < (auxBaseLen)):
                        t = 0
                        #VERIFICA SE O ÍTEM ESTÁ CONTIDO NA LISTA
                        while auxBase[t] in aux:
                            t = t + 1
                        aux.append(auxBase[t])
                        auxBase.remove(auxBase[t])
                        i = i + 1
                        j = j + 1                    
                    auxFinal.append(aux)
                #REMOVE OU NÃO QUESTIONÁRIOS
                removeQuest(auxFinal, subjectQuan, new_questions, subFolderQuest, subFolderInfo)
            elif mix==1:
                i = 0
                j = 0
                t = 0
                while i < (auxBaseLen):
                    j = 0
                    aux = []
                    fixed_questions = random.sample(fixed_questions, len(fixed_questions))
                    while (j < len(fixed_questions)) and (i < (auxBaseLen)):
                        aux.append(fixed_questions[j])
                        j = j + 1
                    j = 0  
                    while (j < (numQuestion - len(fixed_questions))) and (i < (auxBaseLen)):
                        t = 0
                        #VERIFICA SE O ÍTEM ESTÁ CONTIDO NA LISTA
                        while auxBase[t] in aux:
                            t = t + 1
                        aux.append(auxBase[t])
                        auxBase.remove(auxBase[t])
                        i = i + 1
                        j = j + 1                    
                    auxFinal.append(aux)
                #REMOVE OU NÃO QUESTIONÁRIOS
                removeQuest(auxFinal, subjectQuan, new_questions, subFolderQuest, subFolderInfo)

        elif firstLast == 1:
            if mix == 0:
                j = 0
                i = 0
                t = 0
                while i < (auxBaseLen):
                    j = 0
                    aux = []  
                    while (j < (numQuestion - len(fixed_questions))) and (i < (auxBaseLen)):
                        t = 0
                        #VERIFICA SE O ÍTEM ESTÁ CONTIDO NA LISTA
                        while auxBase[t] in aux:
                            t = t + 1
                        aux.append(auxBase[t])
                        auxBase.remove(auxBase[t])
                        i = i + 1
                        j = j + 1   
                    j = 0
                    while (j < len(fixed_questions)):
                        aux.append(fixed_questions[j])
                        j = j + 1               
                    auxFinal.append(aux)
                #REMOVE OU NÃO QUESTIONÁRIOS
                removeQuest(auxFinal, subjectQuan, new_questions, subFolderQuest, subFolderInfo)
            elif mix==1:
                j = 0
                i = 0
                t = 0
                while i < (auxBaseLen):
                    j = 0
                    aux = []
                    while (j < (numQuestion - len(fixed_questions))) and (i < (auxBaseLen)):
                        t = 0
                        #VERIFICA SE O ÍTEM ESTÁ CONTIDO NA LISTA
                        while auxBase[t] in aux:
                            t = t + 1
                        aux.append(auxBase[t])
                        auxBase.remove(auxBase[t])
                        i = i + 1
                        j = j + 1   
                    j = 0
                    fixed_questions = random.sample(fixed_questions, len(fixed_questions))
                    while (j < len(fixed_questions)):
                        aux.append(fixed_questions[j])
                        j = j + 1               
                    auxFinal.append(aux)
                #REMOVE OU NÃO QUESTIONÁRIOS
                removeQuest(auxFinal, subjectQuan, new_questions, subFolderQuest, subFolderInfo)
        elif firstLast == 2:
                j = 0
                i = 0
                t = 0
                while i < (auxBaseLen):
                    j = 0
                    aux = []  
                    while (j < (numQuestion - len(fixed_questions))) and (i < (auxBaseLen)):
                        t = 0
                        #VERIFICA SE O ÍTEM ESTÁ CONTIDO NA LISTA
                        while auxBase[t] in aux:
                            t = t + 1
                        aux.append(auxBase[t])
                        auxBase.remove(auxBase[t])
                        i = i + 1
                        j = j + 1   
                    j = 0
                    while (j < len(fixed_questions)):
                        aux.append(fixed_questions[j])
                        j = j + 1
                    aux = random.sample(aux, len(aux))           
                    auxFinal.append(aux)
                #REMOVE OU NÃO QUESTIONÁRIOS
                removeQuest(auxFinal, subjectQuan, new_questions, subFolderQuest, subFolderInfo)
    subjectQuan=0
    
#PÁGINA para Informações Gerais
elif paginaSelecionada == 'LGQIA+ Informações Gerais':
    st.title("LGQIA+ Informações Gerais")


html = """
        <footer style="border-top: 1px solid black; padding: 20px;">
        <p>Laima - Gerador de Questionários Inteligente com Análise Automatizada (LGQIA+) © 2022-2023 TODOS OS DIREITOS RESERVADOS - Laima - Ufpe</p>
        </footer>
        """

st.markdown(html, unsafe_allow_html=True)

st.empty()  # Cria um espaço vazio no final da página