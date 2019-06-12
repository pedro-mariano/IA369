# IA369
Reprodutibilidade em Pesquisa Computacional

### Instruções para reprodução do paper executável

**1)** Faça o download deste repositório para um diretório local. Caso possua o Git instalado, você também pode clonar o repositório executando o comando a seguir em um terminal: <br>
*$ git clone https://github.com/pedro-mariano/IA369.git*

**2)** Instale os módulos necessários para a execução do paper:

- Python 2.7.16
- Jupyter Notebook 5.7.8 <br>
Ambos podem ser obtidos por meio da instalação do Anaconda, disponível em https://www.anaconda.com/distribution/

- PyGMO 2.11 (https://esa.github.io/pagmo2/install.html)
- DEAP 1.2.2 (https://deap.readthedocs.io/en/master/installation.html) <br>
Siga as instruções de instalação disponíveis nas páginas de cada biblioteca, ou caso possua o pip instalado, execute o seguinte comando em um terminal:<br>
*$ pip install pygmo deap*

**3)** Abra o Jupyter Notebook e execute o arquivo MOMCEDA.ipynb localizado na pasta *deliver/*.

Obs: a execução dos experimentos modifica os arquivos na pasta *dev/files*, que são utilizados para realizar a análise de resultados. Se os experimentos forem interrompidos antes de sua conclusão, a análise de resultados pode apresentar erros. Um back-up dos arquivos originais da pasta *dev/files* está localizado na pasta *dev/files_bkup*.
