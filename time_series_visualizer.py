import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np
np.float = float

register_matplotlib_converters()

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Clean data
# Calcular los percentiles de los límites
lower_limit = df['value'].quantile(0.025)
upper_limit = df['value'].quantile(0.975)

# Filtrar los datos para que queden solo los valores dentro de estos límites
df = df[(df['value'] >= lower_limit) & (df['value'] <= upper_limit)]
print(f"Total rows after cleaning: {len(df)}")

def draw_line_plot():
    # Crear una copia del DataFrame filtrado
    df_copy = df.copy()

    # Configurar el gráfico de líneas
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_copy.index, df_copy['value'], color='skyblue', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Guardar imagen y retornar fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Crear copia y modificar datos para el gráfico de barras mensual
    df_copy = df.copy()
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month

    # Calcular el promedio de visitas por mes y año
    df_bar = df_copy.groupby(['year', 'month'])['value'].mean().unstack()

    # Crear el gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=[
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
])


    # Guardar imagen y retornar fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar datos para los diagramas de caja
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    # Asegurar que la columna 'value' sea de tipo float
    df_box['value'] = df_box['value'].astype('float64')

    # Configurar el tamaño de la figura
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [1, 1]})
    
    # Diagrama de caja por año
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Diagrama de caja por mes
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Guardar imagen y retornar fig
    fig.savefig('box_plot.png')
    return fig