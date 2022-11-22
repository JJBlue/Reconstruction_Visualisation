#version 440

in vec2 texCoord;

uniform sampler2D texture0;

out vec4 out_color;

void main() {
	vec4 color = texture2D(texture0, texCoord.st);
	out_color = vec4(color.rgb, 1.0);
}
