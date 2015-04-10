export LD_LIBRARY_PATH=/jic/software/testing/python/2.7.8/x86_64/lib/:/jic/software/testing/openssl/1.0.1j/x86_64/lib/:$LD_LIBRARY_PATH

python get-pip.py
pip install virtualenv
pip install numpy

unset LDFLAGS
unset CPPFLAGS
bash-4.1$ export BLAS=/jic/software/testing/openblas/0.2.13/x86_64/lib/libopenblas.a 
bash-4.1$ export LAPACK=/jic/software/testing/openblas/0.2.13/x86_64/lib/libopenblas.a 
pip install --install-option="--prefix=/jic/software/testing/scipy/0.15.1/x86_64" scipy==0.15.1
