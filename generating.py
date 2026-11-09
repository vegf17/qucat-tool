import os
import subprocess



#'program_folder'
#'n'
#'module_name'
#'pict_path'可选,默认为 '.'

DATA_FOLDER = "./tools/qucat/data"
RESULT_FOLDER = "./data/results/qucat"

def generate_test_file(config_dic):
    #'/opt/homebrew/Cellar/pict/3.7.4/bin/pict'
    test_root = os.path.join(RESULT_FOLDER, config_dic['module_name'])
    # print(f"\t\tgenerate_test_file (test_root):{test_root}")
    if not os.path.exists(test_root):
        os.makedirs(test_root)
    test_file_root = os.path.join(test_root, 'p'+ str(config_dic['n']) + '.txt')
    # print(f"\t\tgenerate_test_file (test_file_root):{test_file_root}")
    with open(test_file_root,'w') as test_file:
        for i in range(len(config_dic['inputID'])):
            test_file.write('q'+str(config_dic['inputID'][i])+':0,1'+'\n')

def generate_test_suite(config_dic, scenario, k):
    test_root = os.path.join(RESULT_FOLDER, config_dic['module_name'])
    result_root = os.path.join(RESULT_FOLDER, config_dic['module_name'], config_dic['module_name']+ '_'+ scenario)
    # print(f"\t\tgenerate_test_suite (test_root):{test_root}")
    # print(f"\t\tgenerate_test_suite (result_root):{result_root}")
    seedrow = ''
    if config_dic['seedrow'] != '':
        seedrow = ' /e:'+config_dic['seedrow']+' '
    if not os.path.exists(result_root):
        os.makedirs(result_root)
    test_file_root = os.path.join(test_root, 'p' + str(config_dic['n']) + '.txt')
    if not os.path.exists(test_file_root):
        generate_test_file(config_dic)
    test_suite_file = os.path.join(result_root, config_dic['module_name'] + '_input_k' + str(k) + '.txt')
    # print(f"\t\tgenerate_test_suite (test_suite_file):{test_suite_file}")
    # print(f"\t\tgenerate_test_suite (test_file_root):{test_file_root}")

   # print("pict " + test_file_root + " /o:" + str(o) + " /r > " + test_suite_file)
    subprocess.run("pict " + test_file_root + " /o:" + str(k) + seedrow +" /r > " + test_suite_file,
                         shell = True,
                         stdout = subprocess.PIPE,
                         cwd = config_dic['pict_root'])
    # df = pandas.read_csv(test_suite_file,sep='\t')
    # df.to_excel(os.path.join(result_root, config_dic['module_name']+'.xlsx'),sheet_name='input',index=False)
    return test_suite_file
        # D:\WXY\Quantum_CT\inputs_" + str(
        #     K) + "\\" + program + "\\" + mutant + "_o" + str(
        #     o) + "\input_" + program + "_" + mutant + '_' + str(
        #     i) + ".txt")
        #
        # folderGenerating = './inputs_' + str(K) + '/' + program + '/' + mutant + '_o' + str(o) + '/'
        # if not os.path.exists(folderGenerating):
        #     os.makedirs(folderGenerating)
        # for i in range(K):
        #     if n == 10:
        #         print("pict p10.txt /o:" + str(o) + " /r:" + str(Seed_N) + "> D:\WXY\Quantum_CT\inputs_" + str(
        #             K) + "\\" + program + "\\" + mutant + "_o" + str(
        #             o) + "\input_" + program + "_" + mutant + '_' + str(
        #             i) + ".txt")
        #         p = subprocess.Popen(
        #             "pict p10.txt /o:" + str(o) + " /r:" + str(Seed_N) + "> D:\WXY\Quantum_CT\inputs_" + str(
        #                 K) + "\\" + program + "\\" + mutant + "_o" + str(
        #                 o) + "\input_" + program + "_" + mutant + '_' + str(i) + ".txt", shell=True,
        #             stdout=subprocess.PIPE,
        #             cwd="D:\Download\PICT")
        #         Seed_N += 1
        #     if n == 11:
        #         # p = subprocess.Popen("pict p10.txt /o:" + str(o) + " /r> E:\Code\Python_code\Quantum_CT\inputs\input_temp.txt", shell=True,
        #         #                  stdout=subprocess.PIPE, cwd="D:\Download\PICT")
        #         p = subprocess.Popen(
        #             "pict p11.txt /o:" + str(o) + " /r:" + str(Seed_N) + "> D:\WXY\Quantum_CT\inputs_" + str(
        #                 K) + "\\" + program + "\\" + mutant + "_o" + str(
        #                 o) + "\input_" + program + "_" + mutant + '_' + str(i) + ".txt", shell=True,
        #             stdout=subprocess.PIPE,
        #             cwd="D:\Download\PICT")
        #         Seed_N += 1
        #     if n == 7:
        #         # p = subprocess.Popen("pict p10.txt /o:" + str(o) + " /r> E:\Code\Python_code\Quantum_CT\inputs\input_temp.txt", shell=True,
        #         #                  stdout=subprocess.PIPE, cwd="D:\Download\PICT")
        #         p = subprocess.Popen(
        #             "pict p7.txt /o:" + str(o) + " /r:" + str(Seed_N) + "> D:\WXY\Quantum_CT\inputs_" + str(
        #                 K) + "\\" + program + "\\" + mutant + "_o" + str(
        #                 o) + "\input_" + program + "_" + mutant + '_' + str(i) + ".txt", shell=True,
        #             stdout=subprocess.PIPE,
        #             cwd="D:\Download\PICT")
        #         Seed_N += 1


# if __name__ == '__main__':
#     config_dic = {}
#     config_dic['program_folder'] = '/Users/xinyi/Downloads'
#     config_dic['module_name'] = 'entanglement'
#     config_dic['n'] = 3
#     config_dic['o'] = 2
#     config_dic['pict_root'] = '.'
#     test = Generating()
#     test.generate_test_suite(config_dic)
#     test.generate_test_file(config_dic)
#     exe = Executing()
#     exe.comb_testing(config_dic)






