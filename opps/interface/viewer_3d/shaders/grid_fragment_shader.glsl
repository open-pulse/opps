//VTK::System::Dec
//VTK::Output::Dec

in vec3 nearPoint;
in vec3 farPoint;
uniform mat4 MCDCMatrix;
uniform mat4 MCWCMatrix;

vec4 grid(vec3 fragPos3D, float scale) {
    vec2 coord = fragPos3D.xz * scale; // use the scale variable to set the distance between the lines
    vec2 derivative = fwidth(coord);
    vec2 grid = abs(fract(coord - 0.5) - 0.5) / derivative;
    float minimumz = min(derivative.y, 1);
    float minimumx = min(derivative.x, 1);
    bool is_line = min(grid.x, grid.y) < 0.5;

    if (!is_line)
        return vec4(0, 0, 0, 0);

    // z axis
    if(fragPos3D.x > -0.8 * minimumx && fragPos3D.x < 0.8 * minimumx)
        return vec4(0, 0, 1, 1.0);

    // x axis
    if(fragPos3D.z > -0.8 * minimumz && fragPos3D.z < 0.8 * minimumz)
        return vec4(1, 0, 0, 1.0);

    // default line
    return vec4(0.1, 0.1, 0.1, 0.1);
}

float computeDepth(vec3 pos) {
    vec4 clip_space_pos = MCDCMatrix * vec4(pos.xyz, 1.0);
    return ((gl_DepthRange.diff * (clip_space_pos.z / clip_space_pos.w)) +
                gl_DepthRange.near + gl_DepthRange.far) * 0.5;

}

void main() {
    float t = -nearPoint.y / (farPoint.y - nearPoint.y);
    vec3 fragPos3D = nearPoint + t * (farPoint - nearPoint);
    vec4 color = grid(fragPos3D, 1);

    float depth = computeDepth(fragPos3D);
    float fading = max(0, (0.5 - depth / 5));
    color.w *= fading;

    // color.w = 1;
    // color.x = computeDepth(fragPos3D);

    gl_FragDepth = computeDepth(fragPos3D);
    gl_FragColor = color;
}
