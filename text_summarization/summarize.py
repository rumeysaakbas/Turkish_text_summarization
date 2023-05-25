from collections import Counter
import heapq
import re

def summarize_text(text):
    # Metni kelimelere ayırma
    words = re.findall(r'\b\w+\b', text)
    # Kelime frekanslarını hesaplama
    word_freq = Counter(words)
    # Cümleleri bulma
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Cümle skorlarını hesaplama
    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\b\w+\b', sentence):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]
    
    # En önemli cümleleri seçme
    summary_sentences = heapq.nlargest(len(sentences), sentence_scores, key=sentence_scores.get)
    # Özetin cümle sayısını belirleme
    num_sentences = int(len(sentences) * 0.5)  # Cümle sayısının %50'si
    # En önemli cümleleri sıralama
    summary_sentences = summary_sentences[:num_sentences]
    summary_sentences = sorted(summary_sentences, key=lambda x: sentences.index(x))
    
    # Özet metni oluşturma
    summary = ' '.join(summary_sentences)
    return summary



