
from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os, sys
sys.path.append('c:\\codegen\\codegen-service\\server\\source')
import codegen_xml_reader
import codegen_generator_ros
import codegen_generator_opcua


def generate_executable_code(bIsSimulEnv):
	with open('c:\\codegen\\codegen-service\\server\\test.xml', 'r') as file:
		input = file.read()
	xml_parser = codegen_xml_reader.XML_BlocklyProject_Parser(input)
	xml_parser.readAssets()
	slot_val = xml_parser.getList()[0][0]
	outputFileName = 'output/generated_results/'
	# check if real robot mode or simulated OPCUA mode
	# creates either ROS action clients for every found asset OR  
	# creates OPCUA agent for every found asset
	if bIsSimulEnv == 'false':
		ros_gen = codegen_generator_ros.ROSGeneratorClass('_client_py', xml_parser.getList())
		ros_gen.dump_all(outputFileName)
		stream = BytesIO()
		with ZipFile(stream, 'w') as zf:
			for file in glob(os.path.join(outputFileName, '*')):
				zf.write(file, os.path.basename(file))
		stream.seek(0)
		return 'true'
		print ("-----------------------------------------------------")
		print ("Generation of ROS action client files succesfull!")
		print ("-----------------------------------------------------")

		print ("-----------------------------------------------------")
		print ("Generation of OPCUA agent files succesfull!")
		print ("-----------------------------------------------------")
	else:
		return 'Codegen called with incorrect program argument. [bSimulEnv] is not a boolean!'
		print('Codegen called with incorrect program argument. [bSimulEnv] is not a boolean!')
		print('Program execution will stop now...')


if __name__ == "__main__":
    generate_executable_code('false')
