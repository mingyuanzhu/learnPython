#!/usr/bin/env python3
# -*- coding: utf-8 -*-

L1=['Hello','World',18,'Apple',None]
print([x.lower() for x in L1 if isinstance(x,str)])