#version 430

in vec3 normal;
in vec3 frag_pos;

out vec4 out_color;

void main() {
	// Settings
	vec3 light_color = vec3(1.0, 1.0, 1.0);
	vec3 light_dir = vec3(0.0, 1.0, 0.0);
	vec3 object_color = vec3(0.5, 0.5, 0.5);

	// Variables
	vec3 norm = normalize(normal);
	light_dir = normalize(light_dir);

	// Ambient
	float ambient_strength = 0.1;
	vec3 ambient = ambient_strength * light_color;

	// Diffuse
	float diff = max(dot(norm, light_dir), 0.0);
	vec3 diffuse = diff * light_color;

	// Color
	vec3 color = (ambient + diffuse) * object_color;
	out_color = vec4(color, 1.0);
	
	//out_color = vec4(0.5, 0.5, 0.5, 1);
}
