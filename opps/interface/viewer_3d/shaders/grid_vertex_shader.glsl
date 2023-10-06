//VTK::System::Dec
attribute vec4 vertexMC;
//VTK::Normal::Dec
uniform mat4 MCDCMatrix;

out vec3 nearPoint;
out vec3 farPoint;

vec3 UnprojectPoint(float x, float y, float z) {
    vec4 unprojectedPoint =  inverse(MCDCMatrix) * vec4(x, y, z, 1.0);
    return unprojectedPoint.xyz / unprojectedPoint.w;
}

void main () {
    normalVCVSOutput = normalMatrix * normalMC;

    vec4 p = vec4(vertexMC.xyz * 2, 1);
    nearPoint = UnprojectPoint(p.x, p.y, 0).xyz;
    farPoint = UnprojectPoint(p.x, p.y, 1).xyz;

    gl_Position = p;
    // gl_Position = vertexMC;
}
