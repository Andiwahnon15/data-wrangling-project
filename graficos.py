#Grafico circular de Tipos de Formatos
def grafic_types(df):
  import plotly.express as px

  df_count_type = df["type"].value_counts().reset_index()
  fig = px.pie(df_count_type, values='count', names='type', title='Top tipos de formatos de lectura', color_discrete_sequence=px.colors.sequential.RdBu)
  
  fig.show()

#Grafico con los Top 15 generos de libro mas leidos
def grafic_genre(df):
  import plotly.express as px

  df_genre =df[['main_genre', 'sub_genre']].value_counts().reset_index().head(15)
  fig = px.bar(df_genre, x='main_genre', y="count", color='sub_genre',
             title='Top 15 most read genres')
  
  fig.show()

#Grafico de rating por genero
def grafic_rating(df):
  import plotly.express as px

  fig = px.violin(df, y="rating", x="main_genre", box=True, points="all", hover_data=df.columns)
# Adjust the layout
  fig.update_layout(
     height=800,  # Set the height of the graph
     width=1200   # Set the width of the graph
)
  fig.show()

#
def grafic_rated(df):
  import plotly.express as px

  fig = px.scatter(df, x="num_of_people_rated", y="rating", size="price_euro", color="main_genre",
           hover_name="title", log_x=True)
  
  fig.show()

def grafic_correl(df):
  import matplotlib.pyplot as plt
  import seaborn as sns
  import pandas as pd
  
  df_gender = pd.get_dummies(df['main_genre'])
  df_corr = df.merge(df_gender, how="left", left_index=True, right_index=True)
  df_corr.select_dtypes([int, bool, float])
  df_corr.select_dtypes([int, bool, float]).corr()
  sns.set_style("whitegrid")
  plt.figure(figsize=(16, 24))  # Adjusted the size for a vertical orientation
  heatmap = sns.heatmap(df_corr.select_dtypes([int, bool, float]).corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=1, linecolor='white',
            cbar_kws={"shrink": 0.75}, fmt=".2f", annot_kws={"size": 8})  # Reduced annot size for better fit
  heatmap.xaxis.set_ticks_position('top')  # Set the X-axis labels on top
  plt.title('Correlation Heatmap per Department', fontsize=20, pad=40)  # Adjusted padding to accommodate top x-labels
  plt.xticks(fontsize=10, rotation=90, ha='right')
  plt.yticks(fontsize=8, rotation=0)
  plt.tight_layout()
  
  plt.show()

# Uso de tabla de toda la tabla
def grafic_c(df):
  import seaborn as sns

  df_gender = pd.get_dummies(df['main_genre'])
  df_corr = df.merge(df_gender, how="left", left_index=True, right_index=True)

  sns.pairplot(df_corr.select_dtypes([int, bool, float]))




