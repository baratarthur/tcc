import pandas as pd
import matplotlib.pyplot as plt
import os

TIME_CONSTANT = 'time'

def generate_graphic_with_mean(column, key, dirname, filename):
    mean = column.mean()
    line_mean, = plt.plot(range(len(column)), [mean for _ in range(len(column))], 'y')
    line, = plt.plot(range(len(column)), column, 'b')

    plt.title(f"Eixo {key} do arquivo {filename.replace('.csv', '')}")
    plt.legend([line_mean, line], ["mean", "data"])
    
    plt.xlabel("time [s]")
    plt.ylabel("gravity acc [m/s²]")
    plt.ylim(column.min() - 3, column.max() + 3)

    plt.text(0, column.min()- 2, f"mean: {column.mean()}\nvariance: {column.var()}",
            bbox={'facecolor': 'grey', 'alpha': 0.5, 'pad': 5})

    plt.savefig(f"{dirname}/{filename.replace('.csv', '')}_{key}.png")
    plt.clf()

def transform_in_seconds(val):
    return int(val.split(":")[1])*60+int(val.split(":")[2].split('.')[0])

for dirname in os.listdir('csv'):
    print()
    print()
    print('reading: '+dirname)
    for filename in os.listdir('csv/'+dirname):
        print()
        print('== reading file: '+filename)
        dados = pd.read_csv('csv/'+dirname+'/'+filename)

        dados['x'] = dados['x'].apply(float, 1)*9.8
        dados['y'] = dados['y'].apply(float, 1)*9.8
        dados['z'] = dados['z'].apply(float, 1)*9.8

        if TIME_CONSTANT in dados.columns:
            dados[TIME_CONSTANT] = dados[TIME_CONSTANT].apply(transform_in_seconds, 1)
            timeColumn = dados[TIME_CONSTANT]
            dados = dados.groupby(by=TIME_CONSTANT, axis=0).mean()

        print("Media: ", dados['z'].mean())
        print("variancia: ", dados['z'].var())
        locale = f"graficos/{dirname}/{filename.replace('.csv', '')}"

        if dirname == "pistao_sul":
            print("variancia parado:\n", dados[50:90].var())

        try:
            os.mkdir(locale)
        except Exception:
            print(f"Pasta {locale} ja existe")

        generate_graphic_with_mean(dados['z'], 'z', locale, filename)
        generate_graphic_with_mean(dados['x'], 'x', locale, filename)
        generate_graphic_with_mean(dados['y'], 'y', locale, filename)
