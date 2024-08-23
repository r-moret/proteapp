import {
  EditYardOrderSchema,
  YardOrderSchema,
  EditYardSchema,
  YardSchema,
  YardInfoSchema
} from './declarations'

export const EditYardOrderAdapter = (input: any) => EditYardOrderSchema.parse(input)
export const YardOrderAdapter = (input: any) => YardOrderSchema.parse(input)
export const EditYardAdapter = (input: any) => EditYardSchema.parse(input)
export const YardAdapter = (input: any) => YardSchema.parse(input)
export const YardInfoAdapter = (input: any) => YardInfoSchema.parse(input)
