#!/bin/bash
#SBATCH -J chunk_4
#SBATCH -o Outchunk_4.%j.out
#SBATCH -e Errchunk_4.%j.err
#SBATCH -p skx-normal
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 03:00:00
#SBATCH --mail-type=all
#SBATCH -A lph_mem 
#SBATCH --mail-user=majid@utexas.edu


module load python3
module load python3


source /work/05330/jalili/stampede2/goro/gem5/v21/bin/activate


/work/05330/jalili/stampede2/goro/gem5/build/ARM/gem5.opt -d /work/05330/jalili/stampede2/goro/results/multi/mix12 /work/05330/jalili/stampede2/goro/gem5/configs/example/fs.py --caches --kernel /work/05330/jalili/stampede2/goro/disks/binaries/vmlinux.arm64 --disk-image /work/05330/jalili/stampede2/goro/disks/disks/ubuntu-18.04-arm64-docker_big.img --cpu-type=DerivO3CPU --restore-simpoint-checkpoint -r 1 --checkpoint-dir /work/05330/jalili/stampede2/goro/simpoints/ch0/mix12 --restore-with-cpu=AtomicSimpleCPU --l3cache --l3-hwp-type=L3MultiPrefetcher --l2-hwp-type=L2MultiPrefetcher --l1d-hwp-type=L1MultiPrefetcher --mem-size=64GB --mem-type=DDR4_2400_8x8 -n 4 --mode multi > /work/05330/jalili/stampede2/goro/outputs/multi/mix12.out & 
/work/05330/jalili/stampede2/goro/gem5/build/ARM/gem5.opt -d /work/05330/jalili/stampede2/goro/results/multi/mix16 /work/05330/jalili/stampede2/goro/gem5/configs/example/fs.py --caches --kernel /work/05330/jalili/stampede2/goro/disks/binaries/vmlinux.arm64 --disk-image /work/05330/jalili/stampede2/goro/disks/disks/ubuntu-18.04-arm64-docker_big.img --cpu-type=DerivO3CPU --restore-simpoint-checkpoint -r 1 --checkpoint-dir /work/05330/jalili/stampede2/goro/simpoints/ch0/mix16 --restore-with-cpu=AtomicSimpleCPU --l3cache --l3-hwp-type=L3MultiPrefetcher --l2-hwp-type=L2MultiPrefetcher --l1d-hwp-type=L1MultiPrefetcher --mem-size=64GB --mem-type=DDR4_2400_8x8 -n 4 --mode multi > /work/05330/jalili/stampede2/goro/outputs/multi/mix16.out
wait