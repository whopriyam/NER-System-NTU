covid.far: covid.grm covid_symptoms.far place_country.far local_address.far activity.far
	thraxcompiler --input_grammar=$< --output_far=$@

covid_symptoms.far: covid_symptoms.grm example.far exclamation.far numbers.far txt_resource_files/chinesefirstnames.txt txt_resource_files/chineselastnames.txt txt_resource_files/symptom.txt
	thraxcompiler --input_grammar=$< --output_far=$@

example.far: example.grm byte.far numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

byte.far: byte.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

numbers.far: numbers.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

exclamation.far: exclamation.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

place_country.far: place_country.grm example.far numbers.far txt_resource_files/businesses_and_places.txt txt_resource_files/dates.txt txt_resource_files/time.txt txt_resource_files/countries.txt
	thraxcompiler --input_grammar=$< --output_far=$@

local_address.far: local_address.grm example.far numbers.far txt_resource_files/dates.txt txt_resource_files/time.txt txt_resource_files/roads_and_streets.txt txt_resource_files/venues-filtered.txt txt_resource_files/regions.txt
	thraxcompiler --input_grammar=$< --output_far=$@

activity.far: activity.grm example.far numbers.far txt_resource_files/chinesefirstnames.txt txt_resource_files/chineselastnames.txt
	thraxcompiler --input_grammar=$< --output_far=$@

clean:
	rm -f covid_symptoms.far place_country.far local_address.far activity.far example.far exclamation.far numbers.far byte.far
