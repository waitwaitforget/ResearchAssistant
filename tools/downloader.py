import os
import requests
from bs4 import BeautifulSoup

class PaperDownloader(object):
    def __init__(self, save_dir, author_name, scholar_id):
        self.save_dir = save_dir
        self.author_name = author_name
        self.scholar_id = scholar_id
        self.SCHOLAR_BASE_URL = 'https://scholar.google.com/citations?user='
    
    def get_papers_from_profile(self, profile_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        response = requests.get(profile_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        papers = []
        for item in soup.find_all('tr', class_='gsc_a_tr'):
            title = item.find('a', class_='gsc_a_at').text
            link = item.find('a', class_='gsc_a_at')['href']
            
            year = item.find('td', class_='gsc_a_y').text.strip()
            citations = item.find('td', class_='gsc_a_c').text.strip()
            citations = int(citations) if citations.isdigit() else 0  # 转换为整数，若无被引次数则为0
            
            papers.append({
                'title': title, 
                'link': 'https://scholar.google.com' + link,
                'year': year,
                'citations': citations})
        
        return papers

    # 获取论文的PDF链接
    def get_pdf_link(self, paper_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        response = requests.get(paper_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找 [PDF] 链接
        pdf_link = None
        for link in soup.find_all('a'):
            pdf_span = link.find('span', class_='gsc_vcd_title_ggt')
            if pdf_span and pdf_span.text == '[PDF]':
                pdf_link = link['href']
                break
            elif link.text == '[PDF]':
                pdf_link = link['href']
                break
        
        return pdf_link

    def download_paper(self, pdf_url, save_path):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        response = requests.get(pdf_url, headers=headers)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")


    # 主函数
    def download_all_papers(self):
        profile_url = self.SCHOLAR_BASE_URL + self.scholar_id
        # 获取论文列表
        papers = self.get_papers_from_profile(profile_url)
        
        # 创建保存目录
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # 遍历每篇论文
        for paper in papers:
            title = paper['title']
            paper_url = paper['link']
            year = paper['year']
            
            print(f"Processing: {title}")
            
            # 获取PDF链接
            pdf_url = self.get_pdf_link(paper_url)
            #print(paper_url)
            if pdf_url:
                # 下载PDF文件
                save_path = os.path.join(self.save_dir, f"[{year}]{title}.pdf")
                self.download_paper(pdf_url, save_path)
            else:
                print(f"No PDF link found for: {title}")

# 示例使用
def demo():
    # profile_url = 'https://scholar.google.com/citations?user=TGYV2yoAAAAJ'
    scholar_id = "zJEkaG8AAAAJ"
    save_dir='papers/zheweizhang'  # 保存PDF文件的目录

    downloader = PaperDownloader(save_dir, 'zheweizhang', scholar_id)
    downloader.download_all_papers()