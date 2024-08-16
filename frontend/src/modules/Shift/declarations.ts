import { z } from 'zod'
import { IdSchema, type UserInfo } from '../Inform/declarations'
import { createObjectSchema } from '@/utils'

const ShiftTimeSchema = z.enum(['morning', 'afternoon'])
const WeekDaySchema = z.enum([
  'monday',
  'thursday',
  'wednesday',
  'tuesday',
  'friday',
  'saturday',
  'sunday'
])

const ShiftDaySchema = createObjectSchema(ShiftTimeSchema, z.array(IdSchema))
export const ShiftSchema = createObjectSchema(WeekDaySchema, ShiftDaySchema)

export type ShiftTime = z.infer<typeof ShiftTimeSchema>
export type WeekDay = z.infer<typeof WeekDaySchema>
export type Shift = z.infer<typeof ShiftSchema>

export type EnrichedShiftDay = {
  morning: UserInfo[]
  afternoon: UserInfo[]
}

export type EnrichedShift = Record<WeekDay, EnrichedShiftDay>
