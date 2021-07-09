# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


cdef void vInfo(bint verbose, str msg)

cdef void vCall(bint verbose, str func)

cdef void vResponse(bint verbose, str func, res)

cpdef hash_bytestr_iter(bytesiter, hasher)

cpdef hashfile(str fname, char* algo)