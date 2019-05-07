from __future__ import print_function
import math
import random

class Bayes_Classifier:

    pdict = {}
    ndict = {}
    useless = ['e', 'thing', 'can', 'one', 'i\'m', 'everything', 'something', 'u', 'or', 'even', 'also', '.', ',', 'to', 'have', 'they', 'was', '!', '?', 'is', 'a', 'as', 'at', 'had', 'what', 'that', 'i', 'who', 'the', 'an', 'but', 'and', 'where', 'how', 'when', 'why', 'it', 'my', 'saw', 'on', 'it\'s', 'are', 'cinema', 'of', 'using', 'were', 'be', 'action', 'movie', 'because', 'has', 'all', 'this' ,'in', 'than', 'your', 'you', 'if', 'he', 'she', '-', 'do', 'with', 'see', 'been', 'from', 'film', 'these', 'some', 'into', 'went', 'her', 'him', 'his', 'etc', 'guy', 'hers', 'them', 'everyone', 'we', 'ever', ')', '(', 'about', 'theatre', 'by', 'over', 'there']
    pcount = 0.
    ncount = 0.
    pA = 0.
    pB = 0.

    def __init__(self):
        self.pdict = {}
        self.ndict = {}

    def train(self,filename):
        f = open(filename, 'rt')
        lines = f.readlines()

        for line in lines:
            line = line.replace('\n','')
            pn = line.split('|')[1]
            if pn == '5':
                self.pcount = self.pcount + 1
            else:
                self.ncount = self.ncount + 1
            review = line.split('|')[2]
            review = self.removenames(review)
            review = review.lower()
            review = self.trim(review)
            review = self.fix(review)
            review = self.trim(review)
            review = review.split(' ')
            for word in review:
                scale = 1
                if len(review) < 2:
                    scale = 10000
                elif len(review) < 5:
                    scale = 10
                elif len(review) < 15:
                    scale = 6

                if pn == '5':
                    if word in self.pdict:
                        self.pdict[word] = self.pdict[word] + scale
                    else:
                        self.pdict[word] = scale
                else:
                    if word in self.ndict:
                        self.ndict[word] = self.ndict[word] + scale
                    else:
                        self.ndict[word] = 1

        self.pA = float(self.pcount/float(self.pcount + self.ncount))
        self.pB = float(self.ncount/float(self.pcount + self.ncount))
        self.uniquewords = len(self.pdict)
        for key in self.ndict:
            if key not in self.pdict:
                self.uniquewords = self.uniquewords + 1


    def classify(self,filename):
        # code to be completed by student to classifier reviews in file using naive bayes
        # classifier previously trains.  member function must return a list of predicted
        # classes with '5' = positive and '1' = negative
        solution = []
        f = open(filename, 'rt')
        lines = f.readlines()
        # lines = lines[0:200]
        sumP = sum(list(self.pdict.values()))
        sumN = sum(list(self.ndict.values()))

        for line in lines:
            review = line.split('|')[2]
            review = self.removenames(review)
            review = review.lower()
            review = self.trim(review)
            review = self.fix(review)
            review = self.trim(review)
            review = review.split(' ')
            pscore = math.log10(float(self.pA))
            nscore = math.log10(float(self.pB))
            for word in review:
                pscore = pscore + math.log10(float((self.pdict[word] if word in self.pdict else 0) + 1)/float(sumP + self.uniquewords))
                nscore = nscore + math.log10(float((self.ndict[word] if word in self.ndict else 0) + 1)/float(sumN + self.uniquewords))
            if pscore > nscore:
                solution.append('5')
            else:
                solution.append('1')

        return solution

    def fix(self, line):
        line = '. ' + line
        line = line.replace('ies ', 'y ')
        line = line.replace('s ', ' ')
        line = line.replace('es ', 'e ')
        line = line.replace('ed ', 'e ')
        line = line.replace('er ', 'e ')
        line = line.replace('ful ', ' ')
        line = line.replace('ing ', ' ')
        line = line.replace(' bor ', ' boring ')
        line = line.replace('--', ' ')
        line = line.replace('not ', 'not')
        line = line.replace('unfunny', 'notfunny')
        line = line.replace('best picture', 'bestpicture')
        line = line.replace('n\'t ', 'not')
        line = line.replace('-', '')
        line = line.replace('\'re ', ' ')
        return line

    def trim(self,line):
        line = line.split(' ')
        for bad in self.useless:
            while bad in line:
                line.remove(bad)
        line = ' '.join(line)

        return line

    def removenames(self, line):
        line = line.split(' ')
        first = line.pop(0)
        for word in line:
            if len(word) > 3:
                if word[0].isupper() and word[1].islower():
                    while word in line:
                        line.remove(word)
        line = ' '.join(line)
        line = first + ' '+ line
        return line


    
