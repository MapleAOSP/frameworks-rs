#
# Copyright (C) 2015 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

header:
summary: Matrix functions
description:
 These functions let you manipulate square matrices of rank 2x2, 3x3, and 4x4.
 They are particularly useful for graphical transformations and are
 compatible with OpenGL.

 We use a zero-based index for rows and columns.  E.g. the last element of
 a @rs_matrix4x4 is found at (3, 3).

 RenderScript uses column-major matrices and column-based vectors.
 Transforming a vector is done by postmultiplying the vector,
 e.g. <code>(matrix * vector)</code>, as provided by @rsMatrixMultiply().

 To create a transformation matrix that performs two transformations at
 once, multiply the two source matrices, with the first transformation as the
 right argument.  E.g. to create a transformation matrix that applies the
 transformation s1 followed by s2, call <code>rsMatrixLoadMultiply(&combined, &s2, &s1)</code>.
 This derives from <code>s2 * (s1 * v)</code>, which is <code>(s2 * s1) * v</code>.

 We have two style of functions to create transformation matrices:
 rsMatrixLoad<i>Transformation</i> and rsMatrix<i>Transformation</i>.  The
 former style simply stores the transformation matrix in the first argument.
 The latter modifies a pre-existing transformation matrix so that the new
 transformation happens first.  E.g. if you call @rsMatrixTranslate()
 on a matrix that already does a scaling, the resulting matrix when applied
 to a vector will first do the translation then the scaling.
end:

function: rsMatrixGet
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: float
arg: const #1* m, "The matrix to extract the element from."
arg: uint32_t col, "The zero-based column of the element to be extracted."
arg: uint32_t row, "The zero-based row of the element to extracted."
summary: Get one element
description:
 Returns one element of a matrix.

 <b>Warning:</b> The order of the column and row parameters may be unexpected.
test: none
end:

function: rsMatrixInverse
ret: bool
arg: rs_matrix4x4* m, "The matrix to invert."
summary: Inverts a matrix in place
description:
 Returns true if the matrix was successfully inverted.
test: none
end:


function: rsMatrixInverseTranspose
ret: bool
arg: rs_matrix4x4* m, "The matrix to modify."
summary: Inverts and transpose a matrix in place
description:
 The matrix is first inverted then transposed.
 Returns true if the matrix was successfully inverted.
test: none
end:


function: rsMatrixLoad
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: void
arg: #1* destination, "The matrix to set."
arg: const float* array, "The array of values to set the matrix to. These arrays should be 4, 9, or 16 floats long, depending on the matrix size."
summary: Load or copy a matrix
description:
 Set the elements of a matrix from an array of floats or from another matrix.

 If loading from an array, the floats should be in row-major order, i.e. the element a
 <code>row 0, column 0</code> should be first, followed by the element at
 <code>row 0, column 1</code>, etc.

 If loading from a matrix and the source is smaller than the destination, the rest of the
 destination is filled with elements of the identity matrix.  E.g.
 loading a rs_matrix2x2 into a rs_matrix4x4 will give:
 <table style="max-width:300px">
 <tr><td>m00</td> <td>m01</td> <td>0.0</td> <td>0.0</td></tr>
 <tr><td>m10</td> <td>m11</td> <td>0.0</td> <td>0.0</td></tr>
 <tr><td>0.0</td> <td>0.0</td> <td>1.0</td> <td>0.0</td></tr>
 <tr><td>0.0</td> <td>0.0</td> <td>0.0</td> <td>1.0</td></tr>
 </table>
test: none
end:

function: rsMatrixLoad
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: void
arg: #1* destination
arg: const #1* source, "The source matrix."
test: none
end:

function: rsMatrixLoad
t: rs_matrix3x3, rs_matrix2x2
ret: void
arg: rs_matrix4x4* destination
arg: const #1* source
test: none
end:

function: rsMatrixLoadFrustum
ret: void
arg: rs_matrix4x4* m, "The matrix to set."
arg: float left
arg: float right
arg: float bottom
arg: float top
arg: float near
arg: float far
summary: Load a frustum projection matrix
description:
 Constructs a frustum projection matrix, transforming the box
 identified by the six clipping planes <code>left, right, bottom, top,
 near, far</code>.

 To apply this projection to a vector, multiply the vector by the
 created matrix using @rsMatrixMultiply().
test: none
end:

function: rsMatrixLoadIdentity
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: void
arg: #1* m, "The matrix to set."
summary: Load identity matrix
description:
 Set the elements of a matrix to the identity matrix.
test: none
end:

function: rsMatrixLoadMultiply
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: void
arg: #1* m, "The matrix to set."
arg: const #1* lhs, "The left matrix of the product."
arg: const #1* rhs, "The right matrix of the product."
summary: Multiply two matrices
description:
 Sets m to the matrix product of <code>lhs * rhs</code>.

 To combine two 4x4 transformaton matrices, multiply the second transformation matrix
 by the first transformation matrix.  E.g. to create a transformation matrix that applies
 the transformation s1 followed by s2, call
 <code>rsMatrixLoadMultiply(&combined, &s2, &s1)</code>.

 <b>Warning:</b> Prior to version 21, storing the result back into right matrix is not supported and
 will result in undefined behavior.  Use rsMatrixMulitply instead.   E.g. instead of doing
 rsMatrixLoadMultiply (&m2r, &m2r, &m2l), use rsMatrixMultiply (&m2r, &m2l).
 rsMatrixLoadMultiply (&m2l, &m2r, &m2l) works as expected.
test: none
end:

function: rsMatrixLoadOrtho
ret: void
arg: rs_matrix4x4* m, "The matrix to set."
arg: float left
arg: float right
arg: float bottom
arg: float top
arg: float near
arg: float far
summary: Load an orthographic projection matrix
description:
 Constructs an orthographic projection matrix, transforming the box
 identified by the six clipping planes <code>left, right, bottom, top,
 near, far</code> into a unit cube with a corner at
 <code>(-1, -1, -1)</code> and the opposite at <code>(1, 1, 1)</code>.

 To apply this projection to a vector, multiply the vector by the
 created matrix using @rsMatrixMultiply().

 See https://en.wikipedia.org/wiki/Orthographic_projection .
test: none
end:

function: rsMatrixLoadPerspective
ret: void
arg: rs_matrix4x4* m, "The matrix to set."
arg: float fovy, "Field of view, in degrees along the Y axis."
arg: float aspect, "Ratio of x / y."
arg: float near, "The near clipping plane."
arg: float far, "The far clipping plane."
summary: Load a perspective projection matrix
description:
 Constructs a perspective projection matrix, assuming a symmetrical field of view.

 To apply this projection to a vector, multiply the vector by the
 created matrix using @rsMatrixMultiply().
test: none
end:

function: rsMatrixLoadRotate
ret: void
arg: rs_matrix4x4* m, "The matrix to set."
arg: float rot, "How much rotation to do, in degrees."
arg: float x, "The x component of the vector that is the axis of rotation."
arg: float y, "The y component of the vector that is the axis of rotation."
arg: float z, "The z component of the vector that is the axis of rotation."
summary: Load a rotation matrix
description:
 This function creates a rotation matrix.  The axis of rotation is the
 <code>(x, y, z)</code> vector.

 To rotate a vector, multiply the vector by the created matrix
 using @rsMatrixMultiply().

 See http://en.wikipedia.org/wiki/Rotation_matrix .
test: none
end:

function: rsMatrixLoadScale
ret: void
arg: rs_matrix4x4* m, "The matrix to set."
arg: float x, "The multiple to scale the x components by."
arg: float y, "The multiple to scale the y components by."
arg: float z, "The multiple to scale the z components by."
summary: Load a scaling matrix
description:
 This function creates a scaling matrix, where each component of a
 vector is multiplied by a number.  This number can be negative.

 To scale a vector, multiply the vector by the created matrix
 using @rsMatrixMultiply().
test: none
end:

function: rsMatrixLoadTranslate
ret: void
arg: rs_matrix4x4* m, "The matrix to set."
arg: float x, "The number to add to each x component."
arg: float y, "The number to add to each y component."
arg: float z, "The number to add to each z component."
summary: Load a translation matrix
description:
 This function creates a translation matrix, where a
 number is added to each element of a vector.

 To translate a vector, multiply the vector by the created matrix
 using @rsMatrixMultiply().
test: none
end:

function: rsMatrixMultiply
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: void
arg: #1* m, "The left matrix of the product and the matrix to be set."
arg: const #1* rhs, "The right matrix of the product."
summary: Multiply a matrix by a vector or another matrix
description:
 For the matrix by matrix variant, sets m to the matrix product <code>m * rhs</code>.

 When combining two 4x4 transformation matrices using this function, the resulting
 matrix will correspond to performing the rhs transformation first followed by
 the original m transformation.

 For the matrix by vector variant, returns the post-multiplication of the vector
 by the matrix, ie. <code>m * in</code>.

 When multiplying a float3 to a @rs_matrix4x4, the vector is expanded with (1).

 When multiplying a float2 to a @rs_matrix4x4, the vector is expanded with (0, 1).

 When multiplying a float2 to a @rs_matrix3x3, the vector is expanded with (0).

 Starting with API 14, this function takes a const matrix as the first argument.
test: none
end:

function: rsMatrixMultiply
version: 9 13
ret: float4
arg: rs_matrix4x4* m
arg: float4 in
test: none
end:

function: rsMatrixMultiply
version: 9 13
ret: float4
arg: rs_matrix4x4* m
arg: float3 in
test: none
end:

function: rsMatrixMultiply
version: 9 13
ret: float4
arg: rs_matrix4x4* m
arg: float2 in
test: none
end:

function: rsMatrixMultiply
version: 9 13
ret: float3
arg: rs_matrix3x3* m
arg: float3 in
test: none
end:

function: rsMatrixMultiply
version: 9 13
ret: float3
arg: rs_matrix3x3* m
arg: float2 in
test: none
end:

function: rsMatrixMultiply
version: 9 13
ret: float2
arg: rs_matrix2x2* m
arg: float2 in
test: none
end:

function: rsMatrixMultiply
version: 14
ret: float4
arg: const rs_matrix4x4* m
arg: float4 in
test: none
end:

function: rsMatrixMultiply
version: 14
ret: float4
arg: const rs_matrix4x4* m
arg: float3 in
test: none
end:

function: rsMatrixMultiply
version: 14
ret: float4
arg: const rs_matrix4x4* m
arg: float2 in
test: none
end:

function: rsMatrixMultiply
version: 14
ret: float3
arg: const rs_matrix3x3* m
arg: float3 in
test: none
end:

function: rsMatrixMultiply
version: 14
ret: float3
arg: const rs_matrix3x3* m
arg: float2 in
test: none
end:

function: rsMatrixMultiply
version: 14
ret: float2
arg: const rs_matrix2x2* m
arg: float2 in
test: none
end:

function: rsMatrixRotate
ret: void
arg: rs_matrix4x4* m, "The matrix to modify."
arg: float rot, "How much rotation to do, in degrees."
arg: float x, "The x component of the vector that is the axis of rotation."
arg: float y, "The y component of the vector that is the axis of rotation."
arg: float z, "The z component of the vector that is the axis of rotation."
summary: Apply a rotation to a transformation matrix
description:
 Multiply the matrix m with a rotation matrix.

 This function modifies a transformation matrix to first do a rotation.
 The axis of rotation is the <code>(x, y, z)</code> vector.

 To apply this combined transformation to a vector, multiply
 the vector by the created matrix using @rsMatrixMultiply().
test: none
end:

function: rsMatrixScale
ret: void
arg: rs_matrix4x4* m, "The matrix to modify."
arg: float x, "The multiple to scale the x components by."
arg: float y, "The multiple to scale the y components by."
arg: float z, "The multiple to scale the z components by."
summary: Apply a scaling to a transformation matrix
description:
 Multiply the matrix m with a scaling matrix.

 This function modifies a transformation matrix to first do a scaling.
 When scaling, each component of a vector is multiplied by a number.
 This number can be negative.

 To apply this combined transformation to a vector, multiply
 the vector by the created matrix using @rsMatrixMultiply().
test: none
end:

function: rsMatrixSet
t: rs_matrix4x4, rs_matrix3x3, rs_matrix2x2
ret: void
arg: #1* m, "The matrix that will be modified."
arg: uint32_t col, "The zero-based column of the element to be set."
arg: uint32_t row, "The zero-based row of the element to be set."
arg: float v, "The value to set."
summary: Set one element
description:
 Set an element of a matrix.

 <b>Warning:</b> The order of the column and row parameters may be unexpected.
test: none
end:

function: rsMatrixTranslate
ret: void
arg: rs_matrix4x4* m, "The matrix to modify."
arg: float x, "The number to add to each x component."
arg: float y, "The number to add to each y component."
arg: float z, "The number to add to each z component."
summary: Apply a translation to a transformation matrix
description:
 Multiply the matrix m with a translation matrix.

 This function modifies a transformation matrix to first
 do a translation.  When translating, a number is added
 to each component of a vector.

 To apply this combined transformation to a vector, multiply
 the vector by the created matrix using @rsMatrixMultiply().
test: none
end:

function: rsMatrixTranspose
t: rs_matrix4x4*, rs_matrix3x3*, rs_matrix2x2*
ret: void
arg: #1 m, "The matrix to transpose."
summary: Transpose a matrix place
description:
 Transpose the matrix m in place.
test: none
end:
