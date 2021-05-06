import os
import time

def procedure_log(log_filename=''):
	def temp_func(content):
		with open(log_filename+"_log",'a') as f:
			f.write(time.strftime('%Y-%b%d-%H:%M:%S | ',time.localtime())+content+'\n')
	return temp_func

def file_maker(project_folder_name,project):
    if not os.path.isdir('results'):
        os.mkdir('results')
    if not os.path.isdir(f'results/{project_folder_name}'):
        os.mkdir(f'results/{project_folder_name}')
    if not os.path.isdir(f'results/{project_folder_name}/{project}'):
        os.mkdir(f'results/{project_folder_name}/{project}')
    if not os.path.isdir(f'results/{project_folder_name}/done'):
        os.mkdir(f'results/{project_folder_name}/done')