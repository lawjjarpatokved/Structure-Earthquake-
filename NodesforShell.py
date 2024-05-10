import openseespy.opensees as ops
FIXED_NODES=[[0,0,0,1]] ###### Reference: the first 3 are coordinates and 1 is tag
L=B=1

for nodes in FIXED_NODES:
    ops.node(nodes[3]*1e4,*nodes[:3])      ########## node just below column
    ########### nodes for first plate
    ops.node((nodes[3]*1e4)+1,nodes[0],nodes[1]+B/2,nodes[2])
    ops.node((nodes[3]*1e4)+2,nodes[0]+L/2,nodes[1]+B/2,nodes[2])
    ops.node((nodes[3]*1e4)+3,nodes[0]+L/2,nodes[1],nodes[2])


    ####### nodes for 2nd plate
    ops.node((nodes[3]*1e4)+4,nodes[0]+L/2,nodes[1]-B/2,nodes[2])
    ops.node((nodes[3]*1e4)+5,nodes[0],nodes[1]-B/2,nodes[2])


    ops.node((nodes[3]*1e4)+6,nodes[0]-L/2,nodes[1]-B/2,nodes[2])
    ops.node((nodes[3]*1e4)+7,nodes[0]-L/2,nodes[1],nodes[2])

    ops.node((nodes[3]*1e4)+8,nodes[0]-L/2,nodes[1]+B/2,nodes[2])


    ################### Duplicate nodes of corner nodes for assigning soil
    ops.node((nodes[3]*1e4)+2+10,nodes[0]+L/2,nodes[1]+B/2,nodes[2])
    ops.node((nodes[3]*1e4)+4+10,nodes[0]+L/2,nodes[1]-B/2,nodes[2])
    ops.node((nodes[3]*1e4)+6+10,nodes[0]-L/2,nodes[1]-B/2,nodes[2])
    ops.node((nodes[3]*1e4)+8+10,nodes[0]-L/2,nodes[1]+B/2,nodes[2])

    ######### List of node tags for creating plate elements

    node_tags_1st_plate=[nodes[3]*1e4,(nodes[3]*1e4)+1,(nodes[3]*1e4)+2,(nodes[3]*1e4)+3]
    node_tags_2nd_plate=[nodes[3]*1e4,(nodes[3]*1e4)+3,(nodes[3]*1e4)+4,(nodes[3]*1e4)+5]
    node_tags_3rd_plate=[nodes[3]*1e4,(nodes[3]*1e4)+5,(nodes[3]*1e4)+6,(nodes[3]*1e4)+7]
    node_tags_4th_plate=[nodes[3]*1e4,(nodes[3]*1e4)+7,(nodes[3]*1e4)+8,(nodes[3]*1e4)+1]

    ############## list of node pairs for assigning soil springs
    spring_pair1=[(nodes[3]*1e4)+2,(nodes[3]*1e4)+2+10]
    spring_pair2=[(nodes[3]*1e4)+4,(nodes[3]*1e4)+4+10]
    spring_pair3=[(nodes[3]*1e4)+6,(nodes[3]*1e4)+6+10]
    spring_pair4=[(nodes[3]*1e4)+8,(nodes[3]*1e4)+8+10]


    ############# creating elastic membrane plate section
    Make elastic membrane plate section here
    section_tag=10
    
    ############ Creating ShellMITC4 element
    ops.element('ShellMITC4',(nodes[3]*1e5)+1,nodes[3]*1e4,(nodes[3]*1e4)+1,(nodes[3]*1e4)+2,(nodes[3]*1e4)+3)
    ops.element('ShellMITC4',(nodes[3]*1e5)+2,nodes[3]*1e4,(nodes[3]*1e4)+3,(nodes[3]*1e4)+4,(nodes[3]*1e4)+5)
    ops.element('ShellMITC4',(nodes[3]*1e5)+3,nodes[3]*1e4,(nodes[3]*1e4)+5,(nodes[3]*1e4)+6,(nodes[3]*1e4)+7)
    ops.element('ShellMITC4',(nodes[3]*1e5)+4,nodes[3]*1e4,(nodes[3]*1e4)+7,(nodes[3]*1e4)+8,(nodes[3]*1e4)+1)


    Call the funtion to receive the soil parameters , put the same in material definition done few lines below


    ############ Defining PY TZ and QZ material 
    This needs editing 
    mat_tag_py=100
    mat_tag_tz=101
    mat_tag_qz=102
    ops.uniaxialMaterial('PySimple1',mat_tag_py , 2, 4577.81, 0.0066, 0.0)
    ops.uniaxialMaterial('TzSimple1', mat_tag_tz, 2, 0.734, 2.54e-5, 0.0)
    ops.uniaxialMaterial('QzSimple1', mat_tag_qz,  2,  47216.4,  0.00625,  0.0,  0.0)


    ############# creating zero length elements for soil
    ###########  if this throws an error make py and tz springs by using 2 separate commands in both 1 and 2 dof
    ops.element("zeroLength",(nodes[3]*1e4)+2,(nodes[3]*1e4)+2+10,'-mat',*[mat_tag_py,mat_tag_py,mat_tag_tz,mat_tag_tz, mat_tag_qz],'-dir',*[1,2,1,2,3])
    ops.element("zeroLength",(nodes[3]*1e4)+4,(nodes[3]*1e4)+4+10,'-mat',*[mat_tag_py,mat_tag_py,mat_tag_tz,mat_tag_tz, mat_tag_qz],'-dir',*[1,2,1,2,3])
    ops.element("zeroLength",(nodes[3]*1e4)+6,(nodes[3]*1e4)+6+10,'-mat',*[mat_tag_py,mat_tag_py,mat_tag_tz,mat_tag_tz, mat_tag_qz],'-dir',*[1,2,1,2,3])
    ops.element("zeroLength",(nodes[3]*1e4)+8,(nodes[3]*1e4)+8+10,'-mat',*[mat_tag_py,mat_tag_py,mat_tag_tz,mat_tag_tz, mat_tag_qz],'-dir',*[1,2,1,2,3])


    ################# Applying EQ dof command
    ops.equalDOF(nodes[3]*1e4,nodes[3],*[1,2,3,4,5,6])    ###########between column base and footing

    ops.equalDOF((nodes[3]*1e4)+2,nodes[3]*1e4,*[1,2,3,4,5,6])       ############# between shell edge node and shell mid node






    