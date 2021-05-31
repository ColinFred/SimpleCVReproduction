gpu=0

batch_size=1024
seed=0
steps=6
bn="--affine"
cutout="--cutout"
same_shortcut="--sameshortcut"
convbn_type="sample_channel"
Epochs=(250 30 30 30 20)
# LR=(0.025 1e-3 1e-3 4e-3 3.5e-3)
LR=(0.07 0.00283 0.00283 0.01132 0.0099)
WD=(5e-4 0 0 0 0)
distill=("" "" "--distill" "--distill"  "--distill")
distill_lamda=(0 0 2 2 2)
min_lr=(0 5e-4 5e-4 5e-4 5e-4)
alpha_type=("sample_uniform" "sample_trackarch" "sample_trackarch" "sample_trackarch" "sample_trackarch")
track_file=("" "files/Track1_200_archs.json" "files/Track1_200_archs.json" "files/Track1_200_archs.json" "files/Track1_100_archs.json")
resume=("" "train/model.th" "train/model.th" "train/model.th" "train/model.th")
save_dir=("01uniform" "02trackarch" "03distill200" "04distill200" "05distill100")

for(( index = 0; index < 5; index++)); do
    CUDA_VISIBLE_DEVICES=${gpu} \
        python train_supernet.py \
            --batch_size=${batch_size} \
            --seed=${seed} \
            --sample_accumulation_steps=${steps} \
            ${bn} \
            ${cutout} \
            ${same_shortcut} \
            --convbn_type=${convbn_type} \
            --epochs=${Epochs[${index}]} \
            --lr=${LR[${index}]} \
            --weight_decay=${WD[${index}]} \
            ${distill[${index}]} \
            --distill_lamda=${distill_lamda[${index}]} \
            --min_lr=${min_lr[${index}]} \
            --alpha_type=${alpha_type[${index}]} \
            --track_file=${track_file[${index}]} \
            --resume=${resume[${index}]} \
            --save_dir=train/${save_dir[${index}]}
done;
#LR=(0.025 1e-3 1e-3 4e-3 3.5e-3)
