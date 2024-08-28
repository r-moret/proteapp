import { tzDate, parse, isAfter } from '@formkit/tempo'
import { z } from 'zod'
import { get, has, set } from 'lodash'

export function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export function toLocal(time: string) {
  const localTz = Intl.DateTimeFormat().resolvedOptions().timeZone
  const parsedTime = parse(time, 'HH:mm:ssZ')
  return tzDate(parsedTime, localTz)
}

export function shiftType(start: Date) {
  return isAfter(start, parse('14:00:00+02:00', 'HH:mm:ssZ')) ? 'tarde' : 'mañana'
}

export function createObjectSchema<K extends string, V extends z.ZodTypeAny>(
  keysSchema: z.ZodEnum<[K, ...K[]]>,
  valueSchema: V
) {
  return z
    .record(keysSchema, valueSchema)
    .refine((obj): obj is Record<K, z.infer<V>> =>
      keysSchema.options.every((key) => obj[key] != null)
    )
}

export function ImageAdapter<T extends object>(input: T, path: string = 'image') {
  if (has(input, path) && get(input, path)) {
    set(input, path, `${import.meta.env.VITE_BACKEND_URL}/${get(input, path)}`)
  }

  return input
}
