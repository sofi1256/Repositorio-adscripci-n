import numpy as np
import backend as bend

# load data
data = np.loadtxt('experiment_data.txt')
data_t,data_x,data_v = data[:,0],data[:,1],data[:,2]
data_x_sigma,data_v_sigma = 0.3,0.4

# priors

x0_prior = bend.uniform_prior(1.9,2.1)
v0_prior = bend.uniform_prior(-0.75,0.75)
a1_prior = bend.normal_prior(-1.9,2.0)
b1_prior = bend.normal_prior(0.9,0.3)
c21_prior = bend.normal_prior(1.6,1.5)

# parameters

x0 = bend.FittingParameter(2.0,'x0',1,x0_prior)
v0 = bend.FittingParameter(0.0,'v0',1,v0_prior)
a1 = bend.FittingParameter(-1.9, 'a', 1, a1_prior)
b1 = bend.FittingParameter(0.9,'b',1,b1_prior)
c21 = bend.FittingParameter(1.6,'c',(2,1),c21_prior)

parameters = [x0,v0,a1,b1,c21]

# model 2 (velocity)

model2 = bend.VelocityModel(parameters,data_t,data_x,data_v,
                            data_x_sigma,data_v_sigma)

sampler,_,_,_ = model2.setup_sampler(500, 1000, 500)
samples, flat_samples = sampler.get_chain(), sampler.get_chain(flat=True)

label_list = model2.params_labels
bend.cornerplots(flat_samples,label_list)
bend.traceplots(samples,label_list)
bend.autocplots(flat_samples,label_list)

solutions = [np.mean(flat_samples[:,_]) for _ in range(len(parameters))]
model2.plot_simulation(solutions)
