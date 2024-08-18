import { ShiftSchema, ShiftStatusSchema, ShiftActionSchema } from './declarations'

export const ShiftStatusAdapter = (input: any) => ShiftStatusSchema.parse(input)
export const ShiftAdapter = (input: any) => ShiftSchema.parse(input)
export const ShiftActionAdapter = (input: any) => ShiftActionSchema.parse(input)
