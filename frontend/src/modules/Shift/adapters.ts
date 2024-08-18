import { ShiftStatusSchema } from './declarations'

export const ShiftStatusAdapter = (input: any) => ShiftStatusSchema.parse(input)
