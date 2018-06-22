#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:19:32 2018

@author: victorzhang
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
    sid = SentimentIntensityAnalyzer()
    score_dic = sid.polarity_scores('Hi there! I am your new neighbour, nice to meet you')
    m_compound = score_dic['compound']
    m_compound = score_dic['compound']
    m_neg = score_dic['neg']
    m_neu = score_dic['neu']
    m_pos = score_dic['pos']
    print (m_compound)
    print (m_neg)
    print (m_neu)
    print (m_pos)
    
main()