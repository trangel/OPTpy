from os import path, mkdir,curdir
from ..core import Workflow 

__all__ = ['RESPONSESflow']

#   Global variables for this class:
LATMdir="LATM"

class RESPONSESflow(Workflow):
    def __init__(self,**kwargs):
        """ 
        keyword arguments:
        nval : Number of valence bands to compute the response
        nval_total : Total number of valence bands in the NSCF calculation
        nband : Total number of bands in the NSCF calculation
        ncond : Number of conduction bands to calculate the response
        nkTetra : Number of k-points for tetrahedra integration
        scissors=0 : Value of scissors shift (eV) (not working yet)
                     Default = 0.0 eV
        tol: Smearning used in Fermi Golden's rule 
             (Delta function of vc energy difference)
             Default = 0.03 eV
        nspinor : Number of spinorial components
        ecut : Kinetic energy cutoff
        acellz : Dimension (in Bohrs) of unit cell along the z direction
                 Used in layer calculations
        energy_min : Energy minimimum (in eV) in energy grid for responses
                     Default 0
        energy_max : Energy maximum (in eV) in energy grid for responses
                     Default 10 eV
        energy_steps : Number of points in energy grid for responses
                       Default 2001
        lt : total | layer
        components : Tensor components to be calculated, 
             e.g. ["xx","yy","zz"],
        vnlkss=False : Take into accoung Vnl and KSS file (not working yet)
        option: 1 Full #Change name
        smearvalue : Smearing value in eV 
        response : Response to calculate:
        ---------  choose a response ---------
        1  chi1----linear response           24 calChi1-layer linear response     
        3  eta2----bulk injection current    25 calEta2-layer injection current   
        41 zeta----bulk spin injection       29 calZeta-layer spin injection      
        21 shg1L---Length gauge-1w&2w faster 22 shg2L---Length gauge-2w           
        42 shg1V---Velocity gauge-1w&2w      43 shg2V---Velocity gauge-2w         
        44 shg1C---Layer-Length gauge-1w&2w  45 shg2C---Layer-Length gauge-2w     
        26 ndotccp-layer carrier injection   27 ndotvv--carrier injection   
        """
        super(RESPONSESflow, self).__init__(**kwargs)
        self.lt = kwargs['lt']
        self.nval = kwargs['nval']
        self.nval_total = kwargs['nval_total']
        self.ncond = kwargs['ncond']
        self.nband = kwargs['nband']
        self.nkTetra = kwargs['nkTetra']
        self.ecut = kwargs['ecut']
        self.nspinor= kwargs['nspinor']
        self.scissors = kwargs.pop('scissors',0.000)
        self.tol = kwargs.pop('tol',0.03)
        self.acellz = kwargs.pop('acellz',1.000)
        self.energy_min = kwargs.pop('energy_min',0)
        self.energy_max = kwargs.pop('energy_max',10)
        self.energy_steps = kwargs.pop('energy_steps',2001)
        self.components = kwargs['components']
        self.vnlkss = kwargs['vnlkss']
        self.option = kwargs['option']
        self.smearvalue = kwargs['smearvalue']
        self.response = kwargs['response']


    def write_latm_input(self):
        """ Write input files for LATM"""
        from os import path, mkdir,curdir

#       Create LATM dir.:
        if not path.exists(LATMdir):
            mkdir(LATMdir)


#       Get case name:
        self.case=str(self.nkTetra)+"_"+str(int(self.ecut))
        if ( self.nspinor > 1 ):
            self.case = self.case+"-spin"

#       Get variables from input variables:
        components_list=' '.join(str(p) for p in self.components)
        ncond_total=self.nband-self.nval_total
        withSO=".False."
        if ( self.nspinor == 2 ):
            withSO=".True."

#       Get file names:
        energy_data_filename= "eigen_"+self.case
        energys_data_filename= "energys.d_"+self.case
        half_energys_data_filename= "halfenergys.d_"+self.case
        pmn_data_filename= "me_pmn_"+self.case
        rmn_data_filename= "rmn.d_"+self.case
        der_data_filename= "der.d_"+self.case
        tet_list_filename= "tetrahedra_"+self.case
        integrand_filename= "Integrand_"+self.case
        spectrum_filename= "Spectrum_"+self.case
 
#       1. write tmp_$case file:
        filename=LATMdir+"/tmp_"+self.case
        f=open(filename,"w")
#            % (self.lt,case,self.scissors,self.option,self.nval,self.nval_total,self.ncond,ncond_total,self.response,components_list,self.smearvalue,str(self.vnlkss)))
        f.write("&INDATA\n")
        f.write("nVal = %i,\n" % (self.nval))
        f.write("nMax = %i,\n" % (self.nband))
        f.write("nVal_tetra = %i,\n" % (self.nval_total))
        f.write("nMax_tetra = %i,\n" % (self.ncond))
        f.write("kMax = %i,\n" % (self.nkTetra))
        f.write("scissor = %f,\n" % (self.scissors))
        f.write("tol = %f,\n" % (self.tol))
        f.write("nSpinor = %i,\n" % (self.nspinor))
        f.write("acellz = %f,\n" % (self.acellz))
        f.write("withSO = %s,\n" % (withSO))
        f.write("energy_data_filename = \"%s\",\n" % (energy_data_filename))
#       TODO correct misspellings in Tiniba:
        f.write("energys_data_filename = \"%s\",\n" % (energys_data_filename))
        f.write("half_energys_data_filename = \"%s\",\n" % (half_energys_data_filename))
        f.write("pmn_data_filename = \"%s\",\n" % (pmn_data_filename))
        f.write("rmn_data_filename = \"%s\",\n" % (rmn_data_filename))
        f.write("der_data_filename = \"%s\",\n" % (der_data_filename))
        f.write("tet_list_filename = \"%s\",\n" % (tet_list_filename))
        f.write("integrand_filename = \"%s\",\n" % (integrand_filename))
        f.write("spectrum_filename = \"%s\",\n" % (spectrum_filename))
        f.write("energy_min = %i,\n" % (self.energy_min))
        f.write("energy_max = %i,\n" % (self.energy_max))
        f.write("energy_steps = %i\n" % (self.energy_steps))
        f.write("/\n")

        f.close()

    def write_run(self):
        """ Writes file run.sh """
#       run.sh
        filename=LATMdir+"/run.sh"
        f=open(filename,"w")
        f.write("cp ../symmetries/tetrahedra_%i .\n" % (self.nkTetra))
        f.write("cp ../symmetries/Symmetries.Cartesian_%i Symmetries.Cartesian\n" % (self.nkTetra))
        f.write("cp ../eigen_%s .\n" % (self.case))
        f.write("cp ../me_pmn_%s .\n" % (self.case))
        f.close()

    def write_spectra_params(self):
        """ Writes spectra_params file (input for latm executable) """
        from numpy import empty as np_empty
        from numpy import int as np_int

#       Get variables from input variables:
        n_components=len(self.components)
#       Response name
#       1  chi1----linear response           24 calChi1-layer linear response     
#       3  eta2----bulk injection current    25 calEta2-layer injection current   
#       41 zeta----bulk spin injection       29 calZeta-layer spin injection      
#       21 shg1L---Length gauge-1w&2w faster 22 shg2L---Length gauge-2w           
#       42 shg1V---Velocity gauge-1w&2w      43 shg2V---Velocity gauge-2w         
#       44 shg1C---Layer-Length gauge-1w&2w  45 shg2C---Layer-Length gauge-2w     
#       26 ndotccp-layer carrier injection   27 ndotvv--carrier injection 
        responses_dict={
            1  : 'chi1'  , 24 : 'calChi1-layer',
            3  : 'eta2'  , 25 : 'calEta2-layer', 
            41 : 'zeta'  , 29 : 'calZeta-layer' , 
            21 : 'shg1L' , 22 : 'shg2L', 
            26 : 'ndotccp-layer' ,  27 : 'ndotvv',
            42 : 'shg1V' , 43 : 'shg2V',
            44 : 'shg1C' , 45 : 'shg2C' 
}
        components_dict={ 'x' : 1, 'y' : 2, 'z' : 3 }
        resp_name=responses_dict[self.response]
#       spectra.params file:
        filename=LATMdir+"/spectra.params_"+self.case
        f=open(filename,"w")
        f.write("%i\n" % (n_components))
        for ii in range(n_components):
#           Map components 'xyz' to digits '123'
            cc=list(self.components[ii])
            cci=np_empty(shape=(len(cc)),dtype=np_int)
            for jj in range(len(cc)):
                cci[jj]=components_dict[cc[jj]]
#
            resp_filename=resp_name+"."+self.components[ii]+".dat_"+self.case
            file_num=501+ii
            f.write("%i %s %i T\n" % (self.response, resp_filename, file_num))
            for jj in range(len(cc)):
                f.write("%i " % (cci[jj]))
            f.write("\n") 
#1 chi1.xx.dat_385_10-spin 501 T
# 1 1? 
        f.close()       



    def write(self):
        """ Compute optical responses using Tiniba executables"""
        self.write_latm_input()
        self.write_run()
        self.write_spectra_params()
