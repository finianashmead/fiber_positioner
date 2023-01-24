'''this document contains the functions I use to make the plots I use in my research and presentations'''

def position_map(data):
    '''
    this plots the results of the automated test run using the lower-right panel of runFinianGUI.py (the function run_test in the py file)
    as a scatterplot of every fiber tip location recorded in the test, connected in chronological order with black arrows, with data points resulting
    from CH1 triggers in blue and data points resulting from CH2 triggers in green; a dashed red circle is plotted to represent the positioner's
    range of motion, circle parameters were last updated 01/24/23 ;
    data should be the path to that file (a csv), as a string. by default that file is titled test_data
    '''
    #load data
    test_data = pd.read_csv(data)
    #slice by axis 
    ax1slice = test_data['Ax_input'] == 1.0
    ax2slice = test_data['Ax_input'] == 2.0
    ax1data = test_data[ax1slice]
    ax2data = test_data[ax2slice]
    
    #make figure
    xs = test_data['X_pix']
    ys = test_data['Y_pix']
    xs1 = ax1data['X_pix']
    ys1 = ax1data['Y_pix']
    xs2 = ax2data['X_pix']
    ys2 = ax2data['Y_pix']

    fig = plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    #ax.scatter(xs, ys, c='k', alpha=1.)
    ax.scatter(xs1, ys1, c='b', alpha=0.5)
    ax.scatter(xs2, ys2, c='g', alpha=0.5)
    ax.set_xlim(1600., 1920.)
    ax.set_ylim(555., 875.)
    ax.set_xlabel('X_pix')
    ax.set_ylabel('Y_pix')

    ##ROTATE DATA:
    xs2p = ys2
    ys2p = -1*xs2
    m2p, b2p = np.polyfit(xs2p, ys2p, 1)
    m2pr = -1./m2p
    b2pr = -b2p/m2p
    print(m2pr)
    print(b2pr)

    m1, b1 = np.polyfit(xs1, ys1, 1)
    print("SLOPE1: ", m1)
    fit1 = plt.plot(xs1, m1*xs1 + b1, c='r', ls='-.', lw=0.5) 

    #i=0
    #while i < len(xs):
    for i in range(len(xs)-1):
        #print('making arrow')
        ax.arrow(xs[i], ys[i], (xs[i+1]-xs[i]), (ys[i+1]-ys[i]), width=0.5e-4, color='k', head_width=1.2, alpha=0.5, 
                 length_includes_head=True, head_starts_at_zero=True)
    #    i+=1

    #m2, b2 = np.polyfit(xs2, ys2, 1)
    #print("SLOPE2: ", m2)
    #fit2 = plt.plot(xs2, m2pr*xs2 + b2pr, c='r', ls='-.', lw=1.5) 

    circ_1 = plt.Circle((1739,720), 158, color='r', lw=1.5, ls='-.', fill=False)
    ax.add_artist(circ_1)

    m2, b2 = np.polyfit(xs2, ys2, 1)
    print("SLOPE2: ", m2)
    fit2 = plt.plot(xs2, m2*xs2 + b2, c='r', ls='-.', lw=0.5)

    theta1 = np.rad2deg(np.arctan(m1))
    theta2 = np.rad2deg(np.arctan(m2))

    #plt.savefig('fig_name.png')

    print(theta1, theta2, (abs(theta1)+abs(theta2))) 
    
 
def chrono_pix(data):
    '''
    this plots the results of the automated test run using the lower-right panel of runFinianGUI.py (the function run_test in the py file)
    as 4 subplots showing the change in X and Y pixel coordinates during the CH1 and CH2 tests ; data should be the path to that file (a csv), 
    as a string. by default that file is titled test_data
    '''

    #load data
    test_data = pd.read_csv(data)
    #slice by axis 
    ax1slice = test_data['Ax_input'] == 1.0
    ax2slice = test_data['Ax_input'] == 2.0
    ax1data = test_data[ax1slice]
    ax2data = test_data[ax2slice]
    
    #make figures
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2,figsize = (16,10))
    
    ax1.plot(ax1data['X_pix'], label='CH1 X')
    ax1.set_xlabel('trigger #')
    ax1.set_ylabel('X_pix')
    ax1.set_title('CH1 X_pix')
    ax1.legend(loc='upper left')
    
    ax2.plot(ax1data['Y_pix'], label='CH1 Y')
    ax2.set_xlabel('trigger #')
    ax2.set_ylabel('Y_pix')
    ax2.set_title('CH1 Y_pix')
    ax2.legend(loc='upper left')
    
    ax3.plot(ax2data['X_pix'], label='CH2 X')
    ax3.set_xlabel('trigger #')
    ax3.set_ylabel('X_pix')
    ax3.set_title('CH2 X_pix')
    ax3.legend(loc='upper left')
    
    ax4.plot(ax2data['Y_pix'], label='CH2 Y')
    ax4.set_xlabel('trigger #')
    ax4.set_ylabel('Y_pix')
    ax4.set_title('CH2 Y_pix')
    ax4.legend(loc='upper left')  
