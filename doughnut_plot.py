def generate_BAN_doughnut(df, column, seg_colors, wk1, **kwargs):
    
    """
    Function to generate a BAN doughnut plot
    df: dataframe. 
    column: column in df that we want to plot
    seg_colors: list of 4 colors to colour the plot. First colour is the lower quartile and the fourth is the 
    upper quartile
    wk1: index of the row in you you want to plot
    """
    
    unit = ''
    if 'unit' in kwargs:
        unit = kwargs['unit']
    
    # percentiles
    pc_eng_50 = df[column].median()
    pc_eng_25 = np.percentile(np.array(df[column]),25)
    pc_eng_75 = np.percentile(np.array(df[column]),75)

    # Work out the percentile rank of each datapoint
    df['pc_rank'] = df[column].apply(lambda x: stats.percentileofscore(np.array(df[column]),x))
    
    # Set radius of pie chart
    rad0 = 1

    if 'ax' in kwargs:
        ax = kwargs['ax']
    else:
        f, ax = plt.subplots(1,1,figsize=(7,7))
        
    # Set colors based on percentile
    if df.loc[wk1,'pc_rank'] < 25:
        colors0 = seg_colors[0]
    elif (df.loc[wk1,'pc_rank'] < 50):
        colors0 = seg_colors[1]
    elif (df.loc[wk1,'pc_rank'] < 75):
        colors0 = seg_colors[2]
    else:
        colors0 = seg_colors[3]

    colors0 = ['lightgrey']+[colors0]

    ax.pie(
        [100-df.loc[wk1,'pc_rank'],df.loc[wk1,'pc_rank']],
        colors=colors0,
        startangle=90,
        radius=rad0
    )
    my_circle=plt.Circle( (0,0), 0.7*rad0, color='white')

    ax.add_artist(my_circle)

    ax.text(
        0,0,
        str(round(df.loc[wk1,column],2)) + unit,
        horizontalalignment = 'center',
        verticalalignment = 'center',
        fontsize = 70,
        color = colors0[1]
    )

    # --- Add white triangles at 90 degree intervals
    # Set coordinates clockwise from midnight
    # Internal coordinates need to go further into the circle beacause of the curvature

    # Size of indents: h0 = height, b0 = base length
    h0 = 0.03
    b0 = 2*h0/(np.sqrt(3))
    # rotation of coordinates by 90degrees we can multiply by the following matrix
    theta = np.array([[np.math.cos(np.math.pi/2),np.math.sin(np.math.pi/2)],[np.math.sin(np.math.pi/2),-np.math.cos(np.math.pi/2)]])

    # - Midnight, external:
    x1e = [0.5*b0,0,-0.5*b0]
    y1e = [1,1-h0,1]
    xy1e = np.array([x1e,y1e])
    ax.fill(x1e,y1e,'white')
    x1i = [0,0.5*b0*2,-0.5*b0*2]
    y1i = [0.7*rad0+h0,0.7*rad0-h0,0.7*rad0-h0]
    xy1i = np.array([x1i,y1i])
    ax.fill(x1i,y1i,'white')

    # 3 o'clock
    xy1e = np.matmul(theta,xy1e)
    xy1i = np.matmul(theta,xy1i)
    ax.fill(xy1e[0],xy1e[1],'white')
    ax.fill(xy1i[0],xy1i[1],'white')

    # 6 o'clock
    xy1e = np.matmul(theta,xy1e)
    xy1i = np.matmul(theta,xy1i)
    ax.fill(xy1e[0],-xy1e[1],'white')
    ax.fill(xy1i[0],-xy1i[1],'white')

    # 9 o'clock
    xy1e = np.matmul(theta,xy1e)
    xy1i = np.matmul(theta,xy1i)
    ax.fill(-xy1e[0],xy1e[1],'white')
    ax.fill(-xy1i[0],xy1i[1],'white')

    if 'title' in kwargs:
        ax.set_title(kwargs['title'], fontsize = 16, color = 'grey')
    
    if 'ax' not in kwargs:
        plt.show()
    
    if 'filename' in kwargs:
        f.savefig(filename, dpi = 500, bbox_inches = 'tight')
