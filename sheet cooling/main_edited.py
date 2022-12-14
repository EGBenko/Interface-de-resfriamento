import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import simulation_edited as simulation
import select_material_edited as select_material


# **********************************************
# definindo os parâmetros das simulações
n = 0
pause = True  # se pause=True, começa pausado
# geometria da placa
def simula(m1='Cobre',m2='Ouro',m3='Ferro',m4='Bronze',f1='Ar',f2='Ar em movimento',f3='Água',f4='Água em movimento',ti1=100,ti2=100,ti3=100,ti4=100,ts1=800,ts2=800,ts3=800,ts4=800,tf1=400,tf2=400,tf3=400,tf4=400,vs1=1,s1='Python',vs2=1,s2='Python',vs3=2,s3='anel circular',vs4=2,s4='anel circular'):
        
    chapa = simulation.geometry(Lx=1, Ly=1, Lz=5e-3)

    #inicializando a base de dados de materiais:
    db = select_material.material_database('materiais_edited.xls')
    #inicializando a base de dados de fluidos:
    db2 = select_material.fluid_database('materiais_edited.xls')

    # selecionando materiais
    Material1 = db.select(m1)
    Material2 = db.select(m2)
    Material3 = db.select(m3)
    Material4 = db.select(m4)
    # selecionando fluidos
    Fluido1 = db2.select(f1)
    Fluido2 = db2.select(f2)
    Fluido3 = db2.select(f3)
    Fluido4 = db2.select(f4)

    # parâmetros do processo de estampagem
    if vs1 == 1:
        estampa1 = simulation.stamping(Tinitial=ti1, Tstamp=ts1, type=vs1, text=s1, fontsize=90)
    else:
        estampa1 = simulation.stamping(Tinitial=ti1, Tstamp=ts1, type=vs1, forma=s1)
    if vs2 == 1:
        estampa2 = simulation.stamping(Tinitial=ti2, Tstamp=ts2, type=vs2, text=s2, fontsize=90)
    else:
        estampa2 = simulation.stamping(Tinitial=ti2, Tstamp=ts2, type=vs2, forma=s2)
    if vs3 == 1:
        estampa3 = simulation.stamping(Tinitial=ti3, Tstamp=ts3, type=vs3, text=s3, fontsize=90)
    else:
        estampa3 = simulation.stamping(Tinitial=ti3, Tstamp=ts3, type=vs3, forma=s3)
    if vs4 == 1:
        estampa4 = simulation.stamping(Tinitial=ti4, Tstamp=ts4, type=vs4, text=s4, fontsize=90)
    else:
        estampa4 = simulation.stamping(Tinitial=ti4, Tstamp=ts4, type=vs4, forma=s4)
    # list of forma: anel circular / anel elíptico / circulo / furo circular

    # definindo condição de resfriamento/aquecimento
    conv1 = simulation.convection(Trefr=tf1)
    conv2 = simulation.convection(Trefr=tf2)
    conv3 = simulation.convection(Trefr=tf3)
    conv4 = simulation.convection(Trefr=tf4)

    # **********************************************
    # inicializando as simulações 

    simulacao1 = simulation.DiffFin(chapa, Material1, Fluido1, estampa1, conv1)   # ARGUMENTOS:
    simulacao2 = simulation.DiffFin(chapa, Material2,  Fluido2,  estampa2, conv2)  #  1. geommetria
    simulacao3 = simulation.DiffFin(chapa, Material3, Fluido3, estampa3, conv3)   #  2. material 3. fluido
    simulacao4 = simulation.DiffFin(chapa, Material4, Fluido4,  estampa4, conv4) #  4. estampagem 5. convecção

    # **********************************************
    # Gráficos

    fig = plt.figure(figsize=(12, 7), constrained_layout=True)
    plt.suptitle('Resfriamento de chapas finas')

    # função para criar um painel no eixo ax
    def painel(simulacao, ax, titulo=''):

        ax.set_title(titulo)
        ax.set_xlabel(f'$x$ (m)')
        ax.set_ylabel(f'$y$ (m)')

        im = ax.imshow(simulacao.T, vmin=0, vmax=simulacao.stamping.Tstamp, origin='lower', cmap='plasma', extent=(0, simulacao.geometry.Lx, 0, simulacao.geometry.Ly))
        plt.colorbar(im, ax=ax, location='bottom', orientation='horizontal', label='$T$ (°C)', shrink=.5)

        return im

    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 4)
    ax3 = fig.add_subplot(2, 3, 3)
    ax4 = fig.add_subplot(2, 3, 6)

    im1 = painel(simulacao1, ax1, f'{simulacao1.material.name}, {simulacao1.fluid.name}')
    im2 = painel(simulacao2, ax2, f'{simulacao2.material.name}, {simulacao2.fluid.name}')
    im3 = painel(simulacao3, ax3, f'{simulacao3.material.name}, {simulacao3.fluid.name}')
    im4 = painel(simulacao4, ax4, f'{simulacao4.material.name}, {simulacao4.fluid.name}')

    # **********************************************
    # Animação
    
    # Função para pausar com o mouse
    
    def onClick(event):
        global pause
        pause ^= True

    # mostrando o tempo no Painel
    axes2 = plt.subplot(2, 3, 5)
    axes2.axis('off')
    time_label = axes2.text(0.075, 0.2, f'$t = 0$ s', fontsize=40)
    time_label.set_bbox(dict(facecolor='white', alpha=0.5, edgecolor='red'))

    # função de animação
    def animate(i):
        global pause, n
        if not pause:
            for s, im in zip([simulacao1, simulacao2, simulacao3, simulacao4], [im1, im2, im3, im4]):
                s.evolve()
                im.set_array(s.T)
            time_label.set_text(f'$t = {n * simulacao1.dt: .2f}$ s')
            n += 1        
        return  im1, im2, im3, im4, time_label

    delay=0.1
    anim = animation.FuncAnimation(fig, animate, interval=delay, blit=True)

    # custom button
    axes = plt.subplot(2, 3, 2)

    bpause = Button(axes, 'start/pause',color="lightyellow")
    bpause.on_clicked(onClick)


    plt.show()