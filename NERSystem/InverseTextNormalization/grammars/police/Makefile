testrun2.far: testrun2.grm emergency1.far address.far characteristics.far incident.far ages.far phoneno.far icno.far time.far
	thraxcompiler --input_grammar=$< --output_far=$@

emergency1.far: emergency1.grm emergencynoun.far emergencytypev.far dead.far yes-no-confirmation.far address.far commonppl.far pronoun.far
	thraxcompiler --input_grammar=$< --output_far=$@

emergencynoun.far: emergencynoun.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

emergencytypev.far: emergencytypev.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

dead.far: dead.grm numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

numbers.far: numbers.grm byte.far
	thraxcompiler --input_grammar=$< --output_far=$@

byte.far: byte.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

yes-no-confirmation.far: yes-no-confirmation.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

address.far: address.grm numbers.far example.far resources/roads_and_streets.txt resources/venues-filtered.txt resources/regions.txt
	thraxcompiler --input_grammar=$< --output_far=$@

example.far: example.grm byte.far numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

commonppl.far: commonppl.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

pronoun.far: pronoun.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

characteristics.far: characteristics.grm clothes.far colors.far pronoun.far ages.far isdescription.far hasdescription.far
	thraxcompiler --input_grammar=$< --output_far=$@

clothes.far: clothes.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

colors.far: colors.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

ages.far: ages.grm numbers.far time.far
	thraxcompiler --input_grammar=$< --output_far=$@

time.far: time.grm numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

isdescription.far: isdescription.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

hasdescription.far: hasdescription.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

incident.far: incident.grm condition.far weapons.far address.far pronoun.far status.far dead.far
	thraxcompiler --input_grammar=$< --output_far=$@

condition.far: condition.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

weapons.far: weapons.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

status.far: status.grm 
	thraxcompiler --input_grammar=$< --output_far=$@

phoneno.far: phoneno.grm numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

icno.far: icno.grm numbers.far
	thraxcompiler --input_grammar=$< --output_far=$@

clean:
	rm -f emergency1.far address.far characteristics.far incident.far ages.far phoneno.far icno.far time.far emergencynoun.far emergencytypev.far dead.far yes-no-confirmation.far commonppl.far pronoun.far numbers.far byte.far example.far clothes.far colors.far isdescription.far hasdescription.far condition.far weapons.far status.far
