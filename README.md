# IA369
Reprodutibilidade em Pesquisa Computacional

### Instruções para reprodução do paper executável

**1)** Faça o download deste repositório para um diretório local. Caso possua o Git instalado, você também pode clonar o repositório executando o comando a seguir em um terminal: <br>
*$ git clone https://github.com/pedro-mariano/IA369.git*

**2)** Instale os módulos necessários para a execução do paper:

- Python 2.7.16
- Jupyter Notebook 5.7.8 <br>
Ambos podem ser obtidos por meio da instalação do Anaconda, disponível em https://www.anaconda.com/distribution/

- NumPy 1.16.4 (https://www.numpy.org/)
- Matplotlib 2.2.4 (https://matplotlib.org/users/installing.html)
- PyGMO 2.11 (https://esa.github.io/pagmo2/install.html)
- DEAP 1.2.2 (https://deap.readthedocs.io/en/master/installation.html) <br>
Siga as instruções de instalação disponíveis nas páginas de cada biblioteca, ou caso possua o pip instalado, execute o seguinte comando em um terminal:<br>
*$ pip install numpy matplotlib pygmo deap*

**3)** Abra o Jupyter Notebook e execute o arquivo MOMCEDA.ipynb localizado na pasta *deliver/*.

Obs: a execução dos experimentos modifica os arquivos na pasta *dev/files*, que são utilizados para realizar a análise de resultados. Se os experimentos forem interrompidos antes de sua conclusão, a análise de resultados pode apresentar erros. Um back-up dos arquivos originais da pasta *dev/files* está localizado na pasta *dev/files_bkup*.

### Workflow

O workflow do método aqui proposto está representado na figura a seguir. O usuário fornece as funções objetivo que deseja otimizar, bem como as suas preferências que serão utilizadas para classificar soluções candidatas. Além disso, no caso de problemas-teste, a Fronteira de Pareto, que contém as soluções não dominadas do problema, é conhecida e uma amostra de seus pontos também é fornecida para o cálculo de métricas de avaliação do algoritmo. O algoritmo itera sobre uma população de soluções candidatas, inicializada aleatoriamente, cujos indivíduos não-dominados correspondem à saída ao final da execução. Esses indivíduos são utilizados para o cálculo das métricas de avaliação.

<img src="figures/MOMCEDA-workflow.png" class="center">
