import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Netflix Data Analysis Dashboard", layout="wide")

# --- Load and clean data ---
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    
    # Strip spaces and convert to datetime safely
    df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    
    # Fill missing values
    df['rating'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['duration'].fillna('0 min', inplace=True)
    
    return df

df = load_data()

# --- Title ---
st.title("🎬 Netflix Data Exploration Dashboard")
st.markdown("Explore trends in **genres, ratings, durations, and release years** using Netflix dataset.")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
content_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)
country_filter = st.sidebar.selectbox(
    "Select Country",
    options=['All'] + sorted(df['country'].dropna().unique().tolist()),
    index=0
)

filtered_df = df[df['type'].isin(content_type)]
if country_filter != 'All':
    filtered_df = filtered_df[filtered_df['country'].str.contains(country_filter, na=False)]

st.write(f"### Showing {len(filtered_df)} Titles")

# --- 1️⃣ Distribution of Content Type ---
st.subheader("1️⃣ Distribution of Content Type")
fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df, x='type', palette='Set2', ax=ax1)
st.pyplot(fig1)

# --- 2️⃣ Top 10 Popular Genres ---
st.subheader("2️⃣ Top 10 Popular Genres")
filtered_df['listed_in'] = filtered_df['listed_in'].astype(str)
all_genres = filtered_df['listed_in'].str.split(',').explode().str.strip()
top_genres = all_genres.value_counts().head(10)

fig2, ax2 = plt.subplots()
sns.barplot(x=top_genres.values, y=top_genres.index, palette='coolwarm', ax=ax2)
ax2.set_xlabel("Number of Titles")
ax2.set_ylabel("Genre")
st.pyplot(fig2)

# --- 3️⃣ Content Release Trend Over Years ---
st.subheader("3️⃣ Content Release Trend Over Years")
fig3, ax3 = plt.subplots()
sns.histplot(filtered_df['release_year'], bins=30, kde=True, color='teal', ax=ax3)
ax3.set_xlabel("Release Year")
st.pyplot(fig3)

# --- 4️⃣ Top 10 Content Producing Countries ---
st.subheader("4️⃣ Top 10 Content Producing Countries")
top_countries = filtered_df['country'].value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma', ax=ax4)
ax4.set_xlabel("Number of Titles")
ax4.set_ylabel("Country")
st.pyplot(fig4)

# --- 5️⃣ Distribution of Movie Durations ---
st.subheader("5️⃣ Distribution of Movie Durations")
movies = filtered_df[filtered_df['type'] == 'Movie'].copy()
if not movies.empty:
    movies['duration_min'] = movies['duration'].str.replace(' min','').astype(str)
    movies = movies[movies['duration_min'].str.isnumeric()]
    movies['duration_min'] = movies['duration_min'].astype(int)

    fig5, ax5 = plt.subplots()
    sns.histplot(movies['duration_min'], bins=30, kde=True, color='coral', ax=ax5)
    ax5.set_xlabel("Duration (Minutes)")
    st.pyplot(fig5)
else:
    st.info("No movie data available for the selected filters.")

# --- Summary Statistics ---
st.subheader("📊 Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))
