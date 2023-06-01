import gpt_2_simple as gpt2
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1')
lst = gpt2.generate(sess,temperature=0.9,return_as_list=True, length=2047)
lines = lst[0].splitlines()[:-1]
import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-n', type=str, help='name')
args = parser.parse_args()
p1 = args.n
lst2 = [i for i in lines if "<|" and "|>" not in i]
if p1:
    file_name = p1
else:
    file_name = "sample.txt"
with open(file_name, 'a') as file:
    for i, line in enumerate(lst2):
        if i < len(lst2) - 1:
            file.write(line + "\n")
        else:
            file.write(line)
print("The long and difficult sentences are generated and the file name is:",file_name)