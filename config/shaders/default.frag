#version 430

in vec3 normal;
in vec3 frag_pos;

out vec4 out_color;

void main() {
	// Settings
	vec3 light_color = vec3(1.0, 1.0, 1.0);
	vec3 light_dir = vec3(0.5, 1.0, 0.0);
	vec3 object_color = vec3(0.0, 0.5, 0.9);

	// Variables
	vec3 norm_normal = normalize(normal);
	vec3 norm_light_dir = normalize(light_dir);

	// Ambient
	float ambient_strength = 0.3;
	vec3 ambient = ambient_strength * light_color;

	// Diffuse
	float diffuse_strength = 0.5;
	vec3 diffuse = diffuse_strength * light_color * max(dot(norm_normal, norm_light_dir), 0.0);

	// Color
	vec3 color = (ambient + diffuse) * object_color;
	out_color = vec4(color, 1.0);
	
	//out_color = vec4(normal, 1.0);
	//out_color = vec4(0.5, 0.5, 0.5, 1);
}
