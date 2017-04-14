# "queue.pl" uses qsub.  The options to it are
# options to qsub.  If you have GridEngine installed,
# change this to a queue you have access to.
# Otherwise, use "run.pl", which will run jobs locally
# (make sure your --num-jobs options are no more than
# the number of cpus on your machine.

if [ -x /usr/bin/qstat ]; then 
echo Assuming Ponyland config

export train_cmd="queue.pl -q medium"
export decode_cmd="queue.pl -q medium"
export mkgraph_cmd="queue.pl -q medium"
export rnn_cmd="queue.pl -q medium -tc 10"
# the use of cuda_cmd is deprecated, but it's still used in this example
# directory.
export cuda_cmd="queue.pl --gpu 1"

elif [ -x /usr/local/slurm/bin/squeue ]; then
echo Assuming Coma config

export train_cmd="slurm.pl -p normal"
export decode_cmd="slurm.pl -p normal"
export mkgraph_cmd="slurm.pl -p normal"
export rnn_cmd="slurm.pl -p long"
export cuda_cmd="run.pl"

else 
echo "No squeue or qstat found, running local"

export train_cmd=run.pl
export decode_cmd=run.pl
export cuda_cmd=run.pl
export mkgraph_cmd=run.pl

fi


