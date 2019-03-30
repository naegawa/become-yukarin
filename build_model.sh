name="kojima2yukari"
mkdir -p ${name}
cp result_model/predictor_10000.npz ${name}/predictor1.npz
mkdir -p ${name}/o1
mkdir -p ${name}/o2
mkdir -p ${name}/o3
cp result_model_2nd/predictor_10000.npz ${name}/predictor2.npz

cp o1/mean.npy ${name}/o1/
cp o1/var.npy ${name}/o1/
cp o2/mean.npy ${name}/o2/
cp o2/var.npy ${name}/o2/

zip -r ${name}.zip ${name}
