import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json

# Temel stil ayarları
ROSE_PINE_COLORS = {
    'base': "#191724",      # Koyu arka plan
    'surface': "#1f1d2e",   # Biraz daha açık arka plan
    'overlay': "#26233a",   # Grid çizgileri için
    'muted': "#6e6a86",     # Soluk metin
    'subtle': "#908caa",    # Orta ton metin
    'text': "#e0def4",      # Ana metin
    'love': "#eb6f92",      # Pembe
    'gold': "#f6c177",      # Altın
    'rose': "#ebbcba",      # Açık pembe
    'pine': "#31748f",      # Mavi
    'foam': "#9ccfd8",      # Açık mavi
    'iris': "#c4a7e7"       # Mor
}

# Matplotlib stil ayarları
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': ROSE_PINE_COLORS['base'],
    'axes.facecolor': ROSE_PINE_COLORS['base'],
    'axes.edgecolor': ROSE_PINE_COLORS['muted'],
    'axes.labelcolor': ROSE_PINE_COLORS['text'],
    'text.color': ROSE_PINE_COLORS['text'],
    'grid.color': ROSE_PINE_COLORS['overlay'],
    'xtick.color': ROSE_PINE_COLORS['subtle'],
    'ytick.color': ROSE_PINE_COLORS['subtle'],
    'font.size': 14,
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'grid.alpha': 0.2,
})

# Türkçe-İngilizce çeviri sözlüğü
translations = {
    # Genel etiketler
    'Ortalama Not Değişimi': 'Average Grade Change',
    'Dönemler Arası Not Değişimi': 'Grade Change Between Semesters',
    
    # Burs ile ilgili çeviriler
    'Burs Durumuna Göre Dönemler Arası Not Değişimi': 'Grade Change Between Semesters by Scholarship Status',
    'Burs almıyor': 'No Scholarship',
    'Burs alıyor': 'Receives Scholarship',
    
    # Cinsiyet ile ilgili çeviriler
    'Cinsiyete Göre Dönemler Arası Not Değişimi': 'Grade Change Between Semesters by Gender',
    'Kadın': 'Female',
    'Erkek': 'Male',
    
    # Medeni durum ile ilgili çeviriler
    'Medeni Duruma Göre Dönemler Arası Not Değişimi': 'Grade Change Between Semesters by Marital Status',
    
    # Harç ile ilgili çeviriler
    'Harç Ödeme Durumuna Göre Dönemler Arası Not Değişimi': 'Grade Change Between Semesters by Tuition Payment Status',
    'Harç Güncel Değil': 'Tuition Not Current',
    'Harç Güncel': 'Tuition Current',
    
    # Sosyoekonomik faktörler ile ilgili çeviriler
    'Sosyoekonomik Faktörlerin Akademik Başarıya Etkisi': 'Impact of Socioeconomic Factors on Academic Achievement',
    'Etki Büyüklüğü (Korelasyon/Normalize F-istatistiği)': 'Effect Size (Correlation/Normalized F-statistic)',
    'Anne Eğitimi': 'Mother\'s Education',
    'Baba Eğitimi': 'Father\'s Education',
    'Borç Durumu': 'Debt Status',
    'GDP': 'GDP',
    
    # İstatistiksel analizle ilgili çeviriler
    'Faktörlerin İstatistiksel Anlamlılık Düzeyleri': 'Statistical Significance Levels of Factors',
    'p=0.05 eşiği': 'p=0.05 threshold',
    'Cinsiyet': 'Gender',
    'Burs': 'Scholarship',
    'Harç': 'Tuition',
    'Medeni Durum': 'Marital Status',
    
    # Başvuru türü ile ilgili çeviriler
    'Başvuru Türüne Göre Dönemler Arası Not Değişimi': 'Grade Change Between Semesters by Application Type',
    
    # Medeni durum çevirileri
    'Bekar': 'Single',
    'Evli': 'Married',
    'Boşanmış': 'Divorced',
    'Dul': 'Widowed',
    'Birlikte yaşıyor': 'Cohabiting',
    'Yasal olarak ayrı': 'Legally Separated',
    
    # Başvuru türleri çevirileri
    'Kurum/bölüm değişikliği': 'Institution/Department Change',
    'Teknolojik uzmanlık diploma sahipleri': 'Technological Expertise Diploma Holders',
    'Kısa dönem diploma sahipleri': 'Short-term Diploma Holders',
    '3. Aşama - Genel kontenjan': 'Phase 3 - General Quota',
    '23 yaş üstü': 'Over 23 Years Old',
    '1. Aşama - Genel kontenjan': 'Phase 1 - General Quota',
    'Uluslararası öğrenci (lisans)': 'International Student (Undergraduate)',
    '2. Aşama - Genel kontenjan': 'Phase 2 - General Quota'
}

# Değer etiketleme için ortak stil
def add_value_labels(ax, bars, is_horizontal=False, min_threshold=0.01):
    for bar in bars:
        if is_horizontal:
            width = bar.get_width()
            value = width
            # Yatay çubuklar için metin konumu
            if abs(value) < min_threshold:
                # Çok küçük değerler için özel format
                value_text = f'≈{value:.3f}'
            else:
                value_text = f'{value:.2f}'
            
            ax.text(width/2,  # Çubuğun ortasına
                   bar.get_y() + bar.get_height()/2.,
                   value_text,
                   ha='center', 
                   va='center',
                   color=ROSE_PINE_COLORS['base'],
                   fontsize=14,
                   fontweight='bold')
        else:
            height = bar.get_height()
            value = height
            # Dikey çubuklar için metin konumu
            if abs(value) < min_threshold:
                # Çok küçük değerler için özel format
                value_text = f'≈{value:.3f}'
            else:
                value_text = f'{value:.2f}'
            
            ax.text(bar.get_x() + bar.get_width()/2.,
                   height/2,  # Çubuğun ortasına
                   value_text,
                   ha='center',
                   va='center',
                   color=ROSE_PINE_COLORS['base'],
                   fontsize=14,
                   fontweight='bold')

def create_analysis_visualizations(hypothesis_results):
    # 1. Burs Etkisi Analizi
    def create_scholarship_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        scholarship_data = hypothesis_results['academic']['scholarship']['semester_differences']
        
        if lang == 'tr':
            labels = ['Burs almıyor', 'Burs alıyor']
            title = 'Burs Durumuna Göre Dönemler Arası Not Değişimi'
            ylabel = 'Ortalama Not Değişimi'
            filename = 'visualizations/scholarship_effect.png'
        else:
            labels = [translations['Burs almıyor'], translations['Burs alıyor']]
            title = translations['Burs Durumuna Göre Dönemler Arası Not Değişimi']
            ylabel = translations['Ortalama Not Değişimi']
            filename = 'visualizations/scholarship_effect_en.png'
        
        # Veri çubukları
        bars = ax.bar(labels, 
                [scholarship_data['Burs almıyor']['semester_difference'], 
                 scholarship_data['Burs alıyor']['semester_difference']],
                color=[ROSE_PINE_COLORS['love'], ROSE_PINE_COLORS['pine']],
                width=0.6)
        
        # Çubukların üzerine değerleri yazma
        add_value_labels(ax, bars)
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, color=ROSE_PINE_COLORS['text'])
        
        # Grid özelleştirme
        ax.grid(True, axis='y', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        
        # Eksen çizgilerini özelleştirme
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        # Sıfır çizgisi
        ax.axhline(y=0, color=ROSE_PINE_COLORS['muted'], linestyle='--', alpha=0.3, linewidth=1)
        
        # Kenar boşlukları
        plt.tight_layout(pad=3.0)
        
        # Kaydetme
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # 2. Cinsiyet Etkisi Analizi
    def create_gender_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        gender_data = hypothesis_results['demographic']['gender']['semester_differences']
        
        if lang == 'tr':
            labels = ['Kadın', 'Erkek']
            title = 'Cinsiyete Göre Dönemler Arası Not Değişimi'
            ylabel = 'Ortalama Not Değişimi'
            filename = 'visualizations/gender_effect.png'
        else:
            labels = [translations['Kadın'], translations['Erkek']]
            title = translations['Cinsiyete Göre Dönemler Arası Not Değişimi']
            ylabel = translations['Ortalama Not Değişimi']
            filename = 'visualizations/gender_effect_en.png'
        
        # Veri çubukları
        bars = ax.bar(labels, 
                [gender_data['Kadın']['semester_difference'], 
                 gender_data['Erkek']['semester_difference']],
                color=[ROSE_PINE_COLORS['rose'], ROSE_PINE_COLORS['foam']],
                width=0.6)
        
        # Değerleri çubukların üzerine yazma
        add_value_labels(ax, bars)
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_ylabel(ylabel, color=ROSE_PINE_COLORS['text'])
        
        # Grid ve eksen özelleştirmeleri
        ax.grid(True, axis='y', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        plt.tight_layout(pad=3.0)
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # 3. Medeni Durum Analizi
    def create_marital_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        marital_data = hypothesis_results['demographic']['marital_status']['semester_differences']
        
        if lang == 'tr':
            title = 'Medeni Duruma Göre Dönemler Arası Not Değişimi'
            ylabel = 'Ortalama Not Değişimi'
            filename = 'visualizations/marital_status_effect.png'
            labels = list(marital_data.keys())
        else:
            title = translations['Medeni Duruma Göre Dönemler Arası Not Değişimi']
            ylabel = translations['Ortalama Not Değişimi']
            filename = 'visualizations/marital_status_effect_en.png'
            labels = [translations.get(k, k) for k in marital_data.keys()]
        
        # Rose Pine renk paleti ile uyumlu renkler
        colors = [ROSE_PINE_COLORS['love'], ROSE_PINE_COLORS['gold'], 
                 ROSE_PINE_COLORS['pine'], ROSE_PINE_COLORS['foam'], 
                 ROSE_PINE_COLORS['iris'], ROSE_PINE_COLORS['rose']]
        
        bars = ax.bar(labels, 
                [d['semester_difference'] for d in marital_data.values()],
                color=colors[:len(marital_data)])
        
        # Değerleri çubukların üzerine yazma
        add_value_labels(ax, bars)
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_ylabel(ylabel, color=ROSE_PINE_COLORS['text'])
        plt.xticks(rotation=45, ha='right')
        
        # Grid ve eksen özelleştirmeleri
        ax.grid(True, axis='y', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        plt.tight_layout(pad=3.0)
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # 4. Harç Durumu Analizi
    def create_tuition_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        tuition_data = hypothesis_results['socioeconomic']['tuition']['semester_differences']
        
        if lang == 'tr':
            labels = ['Harç Güncel Değil', 'Harç Güncel']
            title = 'Harç Ödeme Durumuna Göre Dönemler Arası Not Değişimi'
            ylabel = 'Ortalama Not Değişimi'
            filename = 'visualizations/tuition_effect.png'
        else:
            labels = [translations['Harç Güncel Değil'], translations['Harç Güncel']]
            title = translations['Harç Ödeme Durumuna Göre Dönemler Arası Not Değişimi']
            ylabel = translations['Ortalama Not Değişimi']
            filename = 'visualizations/tuition_effect_en.png'
        
        # Veri çubukları
        bars = ax.bar(labels, 
                [tuition_data['Harç Güncel Değil']['semester_difference'], 
                 tuition_data['Harç Güncel']['semester_difference']],
                color=[ROSE_PINE_COLORS['gold'], ROSE_PINE_COLORS['foam']],
                width=0.6)
        
        # Değerleri çubukların içine yazma
        add_value_labels(ax, bars)
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_ylabel(ylabel, color=ROSE_PINE_COLORS['text'])
        
        # Grid ve eksen özelleştirmeleri
        ax.grid(True, axis='y', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        plt.tight_layout(pad=3.0)
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # 5. Sosyoekonomik Faktörler Analizi
    def create_socioeconomic_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        socio_factors = {
            'GDP': hypothesis_results['socioeconomic']['gdp']['overall']['correlation'],
            'Anne Eğitimi': hypothesis_results['socioeconomic']['parent_education']['mother']['first_semester']['correlation'],
            'Baba Eğitimi': hypothesis_results['socioeconomic']['parent_education']['father']['first_semester']['correlation'],
            'Borç Durumu': hypothesis_results['socioeconomic']['debtor']['overall']['fStat'] / 100
        }
        
        if lang == 'tr':
            title = 'Sosyoekonomik Faktörlerin Akademik Başarıya Etkisi'
            ylabel = 'Etki Büyüklüğü (Korelasyon/Normalize F-istatistiği)'
            filename = 'visualizations/socioeconomic_factors.png'
            labels = list(socio_factors.keys())
        else:
            title = translations['Sosyoekonomik Faktörlerin Akademik Başarıya Etkisi']
            ylabel = translations['Etki Büyüklüğü (Korelasyon/Normalize F-istatistiği)']
            filename = 'visualizations/socioeconomic_factors_en.png'
            labels = [translations.get(k, k) for k in socio_factors.keys()]
        
        colors = [ROSE_PINE_COLORS['love'], ROSE_PINE_COLORS['gold'], 
                 ROSE_PINE_COLORS['pine'], ROSE_PINE_COLORS['iris']]
        
        bars = ax.bar(labels, socio_factors.values(), color=colors, width=0.5)
        
        # Y ekseni aralığını manuel olarak ayarla
        ax.set_ylim(-0.15, 0.9)
        
        # Değerleri çubukların üstüne yaz
        for bar in bars:
            height = bar.get_height()
            if abs(height) < 0.01:
                value_text = f'≈{height:.3f}'
            else:
                value_text = f'{height:.2f}'
            
            # Pozitif ve negatif değerler için farklı konumlandırma
            if height >= 0:
                y_offset = 0.03  # Pozitif değerler için yukarı
                va = 'bottom'
            else:
                y_offset = -0.03  # Negatif değerler için aşağı
                va = 'top'
            
            ax.text(bar.get_x() + bar.get_width()/2., 
                    height + y_offset,
                    value_text,
                    ha='center',
                    va=va,
                    color=ROSE_PINE_COLORS['text'],
                    fontsize=16,
                    fontweight='bold')
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_ylabel(ylabel, color=ROSE_PINE_COLORS['text'])
        
        # Grid ve eksen özelleştirmeleri
        ax.grid(True, axis='y', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        plt.tight_layout(pad=3.0)
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # 6. İstatistiksel Anlamlılık Analizi
    def create_significance_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        p_values = {
            'Cinsiyet': hypothesis_results['demographic']['gender']['overall']['pValue'],
            'Burs': hypothesis_results['academic']['scholarship']['overall']['pValue'],
            'Harç': hypothesis_results['socioeconomic']['tuition']['overall']['pValue'],
            'Medeni Durum': hypothesis_results['demographic']['marital_status']['overall']['pValue']
        }
        
        if lang == 'tr':
            title = 'Faktörlerin İstatistiksel Anlamlılık Düzeyleri'
            ylabel = '-log10(p-değeri)'
            threshold_label = 'p=0.05 eşiği'
            filename = 'visualizations/statistical_significance.png'
            labels = list(p_values.keys())
        else:
            title = translations['Faktörlerin İstatistiksel Anlamlılık Düzeyleri']
            ylabel = '-log10(p-value)'
            threshold_label = translations['p=0.05 eşiği']
            filename = 'visualizations/statistical_significance_en.png'
            labels = [translations.get(k, k) for k in p_values.keys()]
        
        colors = [ROSE_PINE_COLORS['love'], ROSE_PINE_COLORS['gold'], 
                 ROSE_PINE_COLORS['pine'], ROSE_PINE_COLORS['iris']]
        
        bars = ax.bar(labels, [-np.log10(v) for v in p_values.values()], color=colors)
        
        # Değerleri çubukların üzerine yazma
        add_value_labels(ax, bars)
        
        # Eşik çizgisi
        ax.axhline(y=-np.log10(0.05), color=ROSE_PINE_COLORS['rose'], 
                   linestyle='--', label=threshold_label)
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_ylabel(ylabel, color=ROSE_PINE_COLORS['text'])
        ax.legend(fontsize=12, facecolor=ROSE_PINE_COLORS['surface'], 
                 edgecolor=ROSE_PINE_COLORS['muted'], labelcolor=ROSE_PINE_COLORS['text'])
        
        # Grid ve eksen özelleştirmeleri
        ax.grid(True, axis='y', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        plt.tight_layout(pad=3.0)
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # 7. Başvuru Türü Analizi
    def create_application_plot(lang='tr'):
        # Figür oluşturma
        fig, ax = plt.subplots(figsize=(16, 10))
        fig.patch.set_facecolor(ROSE_PINE_COLORS['base'])
        ax.set_facecolor(ROSE_PINE_COLORS['base'])
        
        app_data = hypothesis_results['enrollment']['application_mode']['semester_differences']
        app_types = list(app_data.keys())[:8]
        app_diffs = [app_data[t]['semester_difference'] for t in app_types]
        
        if lang == 'tr':
            title = 'Başvuru Türüne Göre Dönemler Arası Not Değişimi'
            xlabel = 'Ortalama Not Değişimi'
            filename = 'visualizations/application_mode_effect.png'
            labels = app_types
        else:
            title = translations['Başvuru Türüne Göre Dönemler Arası Not Değişimi']
            xlabel = translations['Ortalama Not Değişimi']
            filename = 'visualizations/application_mode_effect_en.png'
            labels = [translations.get(t, t) for t in app_types]
        
        colors = [ROSE_PINE_COLORS['love'], ROSE_PINE_COLORS['gold'], 
                 ROSE_PINE_COLORS['pine'], ROSE_PINE_COLORS['foam'],
                 ROSE_PINE_COLORS['iris'], ROSE_PINE_COLORS['rose'],
                 ROSE_PINE_COLORS['gold'], ROSE_PINE_COLORS['pine']]
        
        bars = ax.barh(labels, app_diffs, color=colors[:len(app_types)])
        
        # Değerleri çubukların içine yazma
        add_value_labels(ax, bars, is_horizontal=True)
        
        # Stil ayarları
        ax.set_title(title, pad=20, color=ROSE_PINE_COLORS['text'], fontweight='bold')
        ax.set_xlabel(xlabel, color=ROSE_PINE_COLORS['text'])
        
        # Grid ve eksen özelleştirmeleri
        ax.grid(True, axis='x', alpha=0.1, linestyle='--', color=ROSE_PINE_COLORS['overlay'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(ROSE_PINE_COLORS['muted'])
        ax.spines['bottom'].set_color(ROSE_PINE_COLORS['muted'])
        
        plt.tight_layout(pad=3.0)
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                    facecolor=ROSE_PINE_COLORS['base'],
                    edgecolor='none')
        plt.close()
    
    # Her grafik için Türkçe ve İngilizce versiyonları oluştur
    create_scholarship_plot('tr')
    create_scholarship_plot('en')
    
    create_gender_plot('tr')
    create_gender_plot('en')
    
    create_marital_plot('tr')
    create_marital_plot('en')
    
    create_tuition_plot('tr')
    create_tuition_plot('en')
    
    create_socioeconomic_plot('tr')
    create_socioeconomic_plot('en')
    
    create_significance_plot('tr')
    create_significance_plot('en')
    
    create_application_plot('tr')
    create_application_plot('en')

def main():
    # JSON dosyasından verileri oku
    with open('hypothesis_results.json', 'r', encoding='utf-8') as f:
        hypothesis_results = json.load(f)
    
    create_analysis_visualizations(hypothesis_results)

if __name__ == "__main__":
    main()