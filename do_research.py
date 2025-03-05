from tools.downloader import PaperDownloader
from research_assitant import ResearchAssitant

class Pipeline(object):
    
    def __init__(self, author_name, scholar_id):
        self.author_name = author_name
        self.scholar_id = scholar_id
        self.data_dir = './papers/'

    def prepare(self):
        downloader = PaperDownloader(self.data_dir+self.author_name,
                                     author_name=self.author_name,
                                     scholar_id=self.scholar_id)
        downloader.download_all_papers()

    def research(self):
        ra = ResearchAssitant(self.author_name)
        ra.start_analysis(2023, 2024)
        ra.summarize()


if __name__=='__main__':
    scholar_id = "zJEkaG8AAAAJ"
    pipeline = Pipeline('zheweizhang', scholar_id)
    pipeline.prepare()
    pipeline.research()

