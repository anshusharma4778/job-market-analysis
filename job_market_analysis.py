# ============================================================
# Job Market Analysis — Post AI Boom
# Tools: Python, Pandas, Matplotlib, Seaborn
# Dataset: LinkedIn Job Postings (12,217 records)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ── 1. LOAD DATA ─────────────────────────────────────────────
postings = pd.read_csv('job_postings.csv')
skills   = pd.read_csv('job_skills.csv')
summary  = pd.read_csv('job_summary.csv')

# ── 2. MERGE ──────────────────────────────────────────────────
df = postings.merge(skills, on='job_link', how='left')
df = df.merge(summary, on='job_link', how='left')

# ── 3. CLEAN ──────────────────────────────────────────────────
df.drop_duplicates(subset='job_link', inplace=True)
df['job_title']    = df['job_title'].str.strip()
df['job_location'] = df['job_location'].str.strip()
df['job_level']    = df['job_level'].fillna('Not Specified')
df['job_type']     = df['job_type'].fillna('Not Specified')
df['job_skills']   = df['job_skills'].fillna('')

print(f"✅ Dataset ready: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"   Null values remaining: {df.isnull().sum().sum()}")

# ── 4. ANALYSIS ───────────────────────────────────────────────

# 4.1 Top 10 Job Titles
top_titles = df['job_title'].value_counts().head(10)
print("\n📌 Top 10 Job Roles:")
print(top_titles.to_string())

# 4.2 Top 20 Skills
all_skills = []
for s in df['job_skills']:
    all_skills.extend([x.strip() for x in s.split(',') if x.strip()])
skill_counts = Counter(all_skills)
top_skills = pd.Series(dict(skill_counts.most_common(20)))
print("\n📌 Top 10 Skills:")
print(top_skills.head(10).to_string())

# 4.3 Job Type Distribution
print("\n📌 Job Type (Remote vs Onsite vs Hybrid):")
print(df['job_type'].value_counts().to_string())

# 4.4 Job Level Distribution
print("\n📌 Job Level Distribution:")
print(df['job_level'].value_counts().to_string())

# 4.5 Top Companies Hiring
print("\n📌 Top 10 Companies Hiring:")
print(df['company'].value_counts().head(10).to_string())

# 4.6 AI Skills Demand
ai_keywords = ['Machine Learning', 'Deep Learning', 'AI', 'NLP',
                'TensorFlow', 'PyTorch', 'LLM', 'GPT', 'Generative AI']
print("\n📌 AI/ML Skill Mentions in Job Postings:")
for kw in ai_keywords:
    count = df['job_skills'].str.contains(kw, case=False, na=False).sum()
    pct = round(count / len(df) * 100, 1)
    print(f"   {kw}: {count} jobs ({pct}%)")

# ── 5. VISUALIZATIONS ─────────────────────────────────────────
BG = '#F8FAFC'
colors = ['#4F46E5','#7C3AED','#06B6D4','#10B981','#F59E0B',
          '#EF4444','#8B5CF6','#3B82F6','#EC4899','#14B8A6']

fig = plt.figure(figsize=(20, 24), facecolor=BG)
fig.suptitle('Job Market Analysis — Post AI Boom\n12,217 LinkedIn Job Postings',
             fontsize=22, fontweight='bold', color='#1E293B', y=0.98)

# Chart 1: Top Job Titles
ax1 = fig.add_subplot(3, 2, 1)
ax1.barh(top_titles.index[::-1], top_titles.values[::-1], color=colors[:10])
ax1.set_title('Top 10 In-Demand Job Roles', fontweight='bold', fontsize=13)
ax1.set_xlabel('Number of Postings')
ax1.set_facecolor(BG)

# Chart 2: Top Skills
ax2 = fig.add_subplot(3, 2, 2)
ts = top_skills.head(15)
ax2.barh(ts.index[::-1], ts.values[::-1], color='#7C3AED')
ax2.set_title('Top 15 Most Demanded Skills', fontweight='bold', fontsize=13)
ax2.set_xlabel('Frequency in Job Postings')
ax2.set_facecolor(BG)

# Chart 3: Job Type Pie
ax3 = fig.add_subplot(3, 2, 3)
jt = df['job_type'].value_counts()
ax3.pie(jt.values, labels=jt.index, autopct='%1.1f%%',
        colors=['#4F46E5','#06B6D4','#10B981'], startangle=90)
ax3.set_title('Onsite vs Remote vs Hybrid', fontweight='bold', fontsize=13)

# Chart 4: Job Level
ax4 = fig.add_subplot(3, 2, 4)
lc = df['job_level'].value_counts()
ax4.bar(lc.index, lc.values, color=['#4F46E5','#06B6D4'])
ax4.set_title('Job Level Distribution', fontweight='bold', fontsize=13)
ax4.set_ylabel('Number of Postings')
ax4.set_facecolor(BG)

# Chart 5: Top Companies
ax5 = fig.add_subplot(3, 2, 5)
tc = df['company'].value_counts().head(10)
ax5.barh(tc.index[::-1], tc.values[::-1], color='#06B6D4')
ax5.set_title('Top 10 Hiring Companies', fontweight='bold', fontsize=13)
ax5.set_xlabel('Number of Postings')
ax5.set_facecolor(BG)

# Chart 6: AI Skills
ax6 = fig.add_subplot(3, 2, 6)
ai_data = pd.Series({
    'Machine Learning': 2979, 'AI (any)': 5302, 'Deep Learning': 664,
    'TensorFlow': 701, 'PyTorch': 618, 'NLP': 333, 'Generative AI': 179, 'LLM': 252
}).sort_values(ascending=True)
ax6.barh(ai_data.index, ai_data.values, color='#EF4444')
ax6.set_title('AI/ML Skills Demand', fontweight='bold', fontsize=13)
ax6.set_xlabel('Jobs Mentioning Skill')
ax6.set_facecolor(BG)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig('job_market_analysis.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("\n✅ Charts saved to job_market_analysis.png")
