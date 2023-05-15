import analyzer.analyzer as analyzer
import sys

if __name__ == '__main__':
    if(len(sys.argv) < 2):
            print("Give dockerfile as argument")
            exit(1)
    f = sys.argv[1]
    analyzer.runAnalysis(f)    