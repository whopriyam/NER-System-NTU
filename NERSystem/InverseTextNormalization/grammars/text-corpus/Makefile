textcorpus.far: textcorpus.grm hospital.far contact_person_sentences.far hospital_name_sent.far
	thraxcompiler --input_grammar=$< --output_far=$@

hospital.far: hospital.grm example.far exclamation.far designation.far resources/names/chinesefirstnames.txt resources/names/chineselastnames.txt resources/department.txt
	thraxcompiler --input_grammar=$< --output_far=$@

example.far: example.grm byte.far numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

byte.far: byte.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

numbers.far: numbers.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

exclamation.far: exclamation.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

designation.far: designation.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

contact_person_sentences.far: contact_person_sentences.grm example.far exclamation.far resources/medical_attendant.txt resources/names/chinesefirstnames.txt resources/names/chineselastnames.txt
	thraxcompiler --input_grammar=$< --output_far=$@

hospital_name_sent.far: hospital_name_sent.grm example.far exclamation.far resources/singaporehospitals.txt
	thraxcompiler --input_grammar=$< --output_far=$@

clean:
	rm -f hospital.far contact_person_sentences.far hospital_name_sent.far example.far exclamation.far designation.far byte.far numbers.far
