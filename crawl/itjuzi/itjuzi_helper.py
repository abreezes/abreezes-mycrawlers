
class Helper:
    def task(self, url_list, n):
        # 任务切割
        # [[url1,url2....],[]]
        process_url_list = []
        for i in range(n + 1):
            process_url_list.append([])

        # 进程,协程数量
        n = len(process_url_list)
        for i in range(len(url_list)):
            process_url_list[i % n].append(url_list[i])
        return process_url_list

    def gen_url(self,id_list):
        """生成url列表"""
        base_url = 'https://www.itjuzi.com/company/{}'
        url_list = [base_url.format(id[0]) for id in id_list]
        # for id in id_list:
        #     yield self.base_url.format(id[0])
        return url_list

